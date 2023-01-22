# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..models import BlogPost
from web.utils.content import process_content, count_words


BlogPostTranslation = BlogPost._parler_meta.root_model


@receiver(pre_save, sender=BlogPostTranslation)
def blog_post_pre_save(sender, instance: BlogPostTranslation, **kwargs): # pylint: disable=unused-argument
	content = instance.content
	instance.processed_content = process_content(content, instance.language_code)
	instance.words = count_words(content)
