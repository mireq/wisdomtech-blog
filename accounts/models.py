# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_attachments.fields import GalleryField
from django_attachments.models import Library
from parler.models import TranslatedFields

from web.utils.models import TranslatableModel, TranslatableManager


class UserManager(TranslatableManager, BaseUserManager):
	pass


class User(TranslatableModel, AbstractUser):
	objects = UserManager()

	gallery = GalleryField(
		on_delete=models.CASCADE
	)
	links = models.TextField(
		_("Description"),
		help_text=_("Links to other sites e.g twitter: ...(newline)facebook: ..."),
		blank=True,
	)

	translations = TranslatedFields(
		subtitle=models.CharField(
			_("Subtitle"),
			max_length=100,
			blank=True
		),
		short_description=models.TextField(
			_("Short description"),
			blank=True
		),
		description=models.TextField(
			_("Description"),
			blank=True
		),
		processed_description=models.TextField(
			_("Processed description"),
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

	def save(self, *args, **kwargs):
		if self.gallery_id is None:
			self.gallery = Library.objects.create()
		return super().save(*args, **kwargs)

	def get_page_title(self):
		page_title = self.fast_translation_getter('page_title')
		if page_title:
			return page_title
		else:
			return str(self)

	def get_absolute_url(self):
		return reverse('accounts:user_detail', kwargs={'pk': self.pk})
