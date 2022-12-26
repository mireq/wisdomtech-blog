# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_attachments.fields import LibraryField, GalleryField
from django_autoslugfield import AutoSlugField
from parler.models import TranslatedFields

from .managers import BlogPostManager
from web.utils.models import TranslatableModel, TimestampModelMixin


User = get_user_model()


class BlogPost(TimestampModelMixin, TranslatableModel, models.Model):
	objects = BlogPostManager()

	author = models.ForeignKey(
		User,
		verbose_name=_("Author"),
		on_delete=models.PROTECT
	)
	gallery = GalleryField(
		verbose_name=_("Gallery"),
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='+',
	)
	attachments = LibraryField(
		verbose_name=_("Attachments"),
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		related_name='+',
	)
	is_published = models.BooleanField(
		_("Is published"),
		default=False,
	)
	pub_time = models.DateTimeField(
		_("Publication time"),
		blank=True,
		null=True,
		db_index=True
	)

	translations = TranslatedFields(
		title=models.CharField(
			_("Title"),
			max_length=200
		),
		slug=AutoSlugField(
			verbose_name=_("Slug"),
			max_length=200,
			in_respect_to=('pk',),
			reserve_chars=0,
			title_field='title'
		),
		summary=models.TextField(
			_("Summary"),
			blank=True,
		),
		perex=models.TextField(
			_("Perex"),
			blank=True,
		),
		content=models.TextField(
			_("Content"),
			blank=True,
		),
		processed_content=models.TextField(
			_("Processed content"),
			blank=True,
			editable=False,
		),
		page_title=models.CharField(
			_("Page title"),
			max_length=200,
			blank=True
		),
		meta_description=models.TextField(
			_("Meta description"),
			blank=True
		),
	)

	def __str__(self):
		return '%s' % self.fast_translation_getter('title')

	class Meta:
		verbose_name = _("Blog post")
		verbose_name_plural = _("Blog posts")
		ordering = (models.F('pub_time').desc(nulls_last=True), '-id')
		index_together = (('pub_time', 'id'),)
