# -*- coding: utf-8 -*-
from .models import BlogPost
from web.utils.generic_views import ListView, AttachmentListAndUploadView, DetailView


class BlogPostListView(ListView):
	paginate_by = 10

	def get_queryset(self):
		return (BlogPost.objects
			.published()
			.fast_translate(fields=['title', 'slug', 'summary'])
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
