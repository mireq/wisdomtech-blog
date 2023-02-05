# -*- coding: utf-8 -*-
import logging
import shutil
from hashlib import md5
from pathlib import Path

from django.conf import settings
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import translation

from ..models import BlogPost
from web.utils.content import process_content, count_words


logger = logging.getLogger(__name__)

BlogPostTranslation = BlogPost._parler_meta.root_model


def clear_blog_cache(instance: BlogPostTranslation):
	cache_dir = getattr(settings, 'NGINX_CACHE_DIR', None)
	if cache_dir is None:
		return
	cache_dir = Path(cache_dir)

	with translation.override(instance.language_code):
		url = reverse('blog:post_detail', kwargs={'slug': instance.slug, 'pk': instance.master_id})
		hash_value = md5(url.encode('utf-8')).hexdigest()
		filename = cache_dir / hash_value[-1] / hash_value[-3:-1] / hash_value
		filename.unlink(missing_ok=True)

	if (cache_dir / 'list').is_dir():
		shutil.rmtree(cache_dir / 'list')



@receiver(pre_save, sender=BlogPostTranslation)
def blog_post_pre_save(sender, instance: BlogPostTranslation, **kwargs): # pylint: disable=unused-argument
	content = instance.content
	instance.processed_content = process_content(content, instance.language_code)
	instance.words = count_words(content)


@receiver(post_save, sender=BlogPostTranslation)
@receiver(post_delete, sender=BlogPostTranslation)
def blog_post_post_save(sender, instance: BlogPostTranslation, **kwargs): # pylint: disable=unused-argument
	try:
		clear_blog_cache(instance)
	except BaseException:
		logger.exception("Cache not cleared")
