# -*- coding: utf-8 -*-
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from blog.models import BlogPost


class BlogModelTest(TestCase):
	def test_publisehd(self):
		now = timezone.now()

		# published in past
		blog = baker.make(BlogPost, is_published=True, pub_time=now - timedelta(1)) # 1 day in past
		self.assertEqual(1, BlogPost.objects.published().filter(pk=blog.pk).count())

		# disabled publication status
		blog.is_published = False
		blog.save(update_fields=['is_published'])
		self.assertEqual(0, BlogPost.objects.published().filter(pk=blog.pk).count())

		# publication time not set - don't show
		blog.is_published = True
		blog.pub_time = None
		blog.save(update_fields=['is_published', 'pub_time'])
		self.assertEqual(0, BlogPost.objects.published().filter(pk=blog.pk).count())

		# publication time in future
		blog.is_published = True
		blog.pub_time = now + timedelta(1)
		blog.save(update_fields=['is_published', 'pub_time'])
		self.assertEqual(0, BlogPost.objects.published().filter(pk=blog.pk).count())
