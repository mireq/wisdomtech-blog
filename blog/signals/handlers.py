# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

import shutil
from pathlib import Path
from django.conf import settings
from ..models import BlogPost
from web.utils.content import process_content, count_words
import logging


logger = logging.getLogger(__name__)

BlogPostTranslation = BlogPost._parler_meta.root_model


def clear_blog_cache(instance: BlogPostTranslation):
	cache_dir = getattr(settings, 'NGINX_CACHE_DIR', None)
	if cache_dir is None:
		return

	cache_dir = Path(cache_dir)
	if (cache_dir / 'list').is_dir():
		shutil.rmtree(cache_dir / 'list')

	# TODO: language prefix



@receiver(pre_save, sender=BlogPostTranslation)
def blog_post_pre_save(sender, instance: BlogPostTranslation, **kwargs): # pylint: disable=unused-argument
	content = instance.content
	instance.processed_content = process_content(content, instance.language_code)
	instance.words = count_words(content)

	try:
		clear_blog_cache(instance)
	except BaseException:
		logger.exception("Cache not cleared")
