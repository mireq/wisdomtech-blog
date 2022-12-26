# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from parler.managers import TranslatableQuerySet


class BlogPostQuerySet(TranslatableQuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(is_published=True, pub_time__isnull=False, pub_time__lte=now)


BlogPostManager = models.Manager.from_queryset(BlogPostQuerySet)
