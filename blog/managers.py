# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Prefetch
from django.utils import timezone

from web.utils.models import TranslatableQuerySet


class BlogPostQuerySet(TranslatableQuerySet):
	def published(self):
		now = timezone.now()
		return self.filter(is_published=True, pub_time__isnull=False, pub_time__lte=now)

	def prefetch_category(self):
		Category = self.model._meta.get_field('category').related_model
		categories = Prefetch('category', Category.objects.fast_translate(self._language))
		return self.prefetch_related(categories)



BlogPostManager = models.Manager.from_queryset(BlogPostQuerySet)
