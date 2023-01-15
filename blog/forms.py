# -*- coding: utf-8 -*-
from django_attachments.models import Library
from parler.forms import TranslatableModelForm
from django.urls import reverse

from .models import BlogPost
from web.utils.widgets import RichTextWidget


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
		widgets = {
			'summary': RichTextWidget(config='basic'),
			'perex': RichTextWidget(config='basic'),
			'content': RichTextWidget(config='content'),
		}
