# -*- coding: utf-8 -*-
from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_attachments.models import Library
from parler.forms import TranslatableModelForm

from .models import BlogPost, BlogCategory, BlogTag
from web.utils.widgets import RichTextWidget


class BlogCategoryForm(TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['slug'].required = False

	class Meta:
		model = BlogCategory
		fields = ['title', 'slug', 'page_title', 'meta_description']


class BlogTagForm(TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['slug'].required = False

	class Meta:
		model = BlogCategory
		fields = ['title', 'slug']


class BlogPostForm(TranslatableModelForm):
	blog_tags = forms.CharField(
		label=_("Blog tags"),
		help_text=_("Separated with comma charracter"),
		required=False,
	)

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
			self.fields['category'].queryset = (BlogCategory.objects
				.fast_translate(self.instance.language_code, fallback=True)
				.order_by('fast_translation_title'))
		if 'blog_tags' in self.fields:
			if self.instance.pk:
				tags = (self.instance.tags
					.fast_translate(self.instance.language_code, fallback=True)
					.values_list('fast_translation_title', flat=True))
				self.initial['blog_tags'] = ', '.join(tags)

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

	def _save_m2m(self, *args, **kwargs):
		requested_tags = self.cleaned_data.get('blog_tags', '').split(',')
		requested_tags = {tag.strip() for tag  in requested_tags if tag.strip()}

		tag_map = dict(BlogTag.objects
			.fast_translate(self.instance.language_code, fallback=True)
			.filter(fast_translation_title__in=requested_tags)
			.values_list('fast_translation_title', 'pk'))

		tags_to_create = requested_tags - set(tag_map.keys())
		for tag in tags_to_create:
			instance = BlogTag()
			instance.set_current_language(self.instance.language_code)
			instance.title = tag
			instance.save()
			tag_map[tag] = instance.pk

		current_tags = set(self.instance.tags.values_list('pk', flat=True))
		assign_tags = set(tag_map.values()) - current_tags
		unassign_tags = current_tags - set(tag_map.values())

		m2m_model = BlogPost._meta.get_field('tags').remote_field.through
		if unassign_tags:
			m2m_model.objects.filter(blogpost_id=self.instance.pk, blogtag_id__in=unassign_tags).delete()
		if assign_tags:
			objs = []
			for tag_id in assign_tags:
				objs.append(m2m_model(blogpost_id=self.instance.pk, blogtag_id=tag_id))
			m2m_model.objects.bulk_create(objs)

		return super()._save_m2m(*args, **kwargs)

	class Meta:
		model = BlogPost
		fields = ['title', 'slug', 'category', 'is_published', 'pub_time', 'summary', 'perex', 'content', 'gallery', 'attachments', 'page_title', 'meta_description']
		widgets = {
			'summary': RichTextWidget(config='basic'),
			'perex': RichTextWidget(config='basic'),
			'content': RichTextWidget(config='content'),
		}
