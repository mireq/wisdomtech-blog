# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from .models import BlogPost, BlogCategory
from web.utils.generic_views import ListView, AttachmentListAndUploadView, DetailView, RedirectOnBadSlugMixin


class BlogPostListView(ListView):
	def get_paginate_by(self, queryset): # pylint: disable=unused-argument
		if 'page' in self.request.GET:
			return 10
		else:
			return 9

	def get_queryset(self):
		return (BlogPost.objects
			.published()
			.fast_translate(fields=['title', 'slug', 'summary', 'words'])
			.select_related('gallery', 'gallery__primary_attachment')
		)


class CategoryBlogPostListView(RedirectOnBadSlugMixin, BlogPostListView):
	def get_object(self):
		obj = getattr(self, 'object', None)
		if obj is None:
			obj = get_object_or_404(BlogCategory.objects.fast_translate(), pk=self.kwargs['pk'])
			self.object = obj
		return obj

	def get_queryset(self):
		return super().get_queryset().filter(category=self.get_object())

	def get_context_data(self, **kwargs):
		return super().get_context_data(object=self.get_object(), **kwargs)


class BlogPostAttachmentsList(AttachmentListAndUploadView):
	model_class = BlogPost


class BlogPostDetailView(DetailView):
	def get_queryset(self):
		return (BlogPost.objects
			.published()
			.prefetch_category()
			.fast_translate()
			.select_related('gallery', 'gallery__primary_attachment')
		)
