# -*- coding: utf-8 -*-
from .models import BlogPost
from web.utils.generic_views import ListView, AttachmentListAndUploadView, DetailView


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


class BlogPostAttachmentsList(AttachmentListAndUploadView):
	model_class = BlogPost


class BlogPostDetailView(DetailView):
	def get_queryset(self):
		return (BlogPost.objects
			.published()
			.fast_translate()
			.select_related('gallery', 'gallery__primary_attachment')
		)
