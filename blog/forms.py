# -*- coding: utf-8 -*-
from django.urls import reverse
from django_attachments.models import Library
from parler.forms import TranslatableModelForm

from .models import BlogPost, BlogCategory
from web.utils.widgets import RichTextWidget


class BlogCategoryForm(TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['slug'].required = False

	class Meta:
		model = BlogCategory
		fields = ['title', 'slug', 'page_title', 'meta_description']


class BlogPostForm(TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['gallery'].required = False
		self.fields['attachments'].required = False
		self.fields['slug'].required = False
		if self.instance and self.instance.pk:
			url = reverse('blog:post_attachments', kwargs={'pk': self.instance.pk})
			self.fields['content'].widget.set_edit_url(url)
		self.fields['author'].required = False
		if 'category' in self.fields:
			self.fields['category'].queryset = BlogCategory.objects.fast_translate(fallback=True).order_by('fast_translation_title')

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
		fields = ['title', 'slug', 'category', 'is_published', 'pub_time', 'summary', 'perex', 'content', 'gallery', 'attachments', 'page_title', 'meta_description']
		widgets = {
			'summary': RichTextWidget(config='basic'),
			'perex': RichTextWidget(config='basic'),
			'content': RichTextWidget(config='content'),
		}
