# -*- coding: utf-8 -*-
from django_attachments.models import Library
from parler.forms import TranslatableModelForm

from .models import BlogPost


class BlogPostForm(TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['gallery'].required = False
		self.fields['attachments'].required = False
		self.fields['slug'].required = False

	def save(self, commit=True):
		obj = super().save(commit=False)
		if not hasattr(obj, 'gallery'):
			lib = Library()
			lib.save()
			obj.gallery = lib
		if not hasattr(obj, 'attachments'):
			lib = Library()
			lib.save()
			obj.attachments = lib
		if commit:
			obj.save()
		return obj

	class Meta:
		model = BlogPost
		fields = ['title', 'slug', 'is_published', 'pub_time', 'summary', 'perex', 'content', 'gallery', 'attachments', 'page_title', 'meta_description']
