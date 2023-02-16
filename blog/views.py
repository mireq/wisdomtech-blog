# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .models import BlogPost, BlogCategory
from web.utils.generic_views import ListView, AttachmentListAndUploadView, DetailView, RedirectOnBadSlugMixin


User = get_user_model()


class BlogPostListView(ListView):
	QUERYSET = (BlogPost.objects
		.select_related('gallery', 'gallery__primary_attachment', 'author')
		.only('pk', 'pub_time', 'author__id', 'author__first_name', 'author__last_name', 'author__username', 'gallery__id', 'gallery__primary_attachment__id', 'gallery__primary_attachment__file')
	)

	def get_paginate_by(self, queryset): # pylint: disable=unused-argument
		if 'page' in self.request.GET:
			return 10
		else:
			return 9

	def get_queryset(self):
		return self.QUERYSET.fast_translate(fields=['title', 'slug', 'summary', 'words']).published()


class BlogPostFeed(Feed):
	title = _("Articles")
	link = reverse_lazy('blog:post_list')

	@cached_property
	def category_translations(self):
		return dict(BlogCategory.objects.fast_translate(fields=['title']).values_list('pk', 'fast_translation_title'))

	def items(self, obj):
		qs = (BlogPost.objects
			.published()
			.fast_translate(fields=['title', 'slug', 'summary'])
			.values('pk', 'fast_translation_title', 'fast_translation_slug', 'fast_translation_summary', 'pub_time', 'date_updated', 'author__username', 'author__first_name', 'author__last_name', 'category_id')
		)
		if obj is not None:
			if isinstance(obj, BlogCategory):
				qs = qs.filter(category=obj)
			elif isinstance(obj, User):
				qs = qs.filter(author=obj)
		return qs

	def get_object(self, request, pk=None, slug=None, user_id=None): # pylint: disable=unused-argument
		if pk is None and user_id is None:
			return None
		if pk is not None:
			return get_object_or_404(BlogCategory.objects.fast_translate(), pk=pk)
		return get_object_or_404(User.objects.filter(is_active=True), pk=user_id)

	def item_title(self, obj):
		return obj['fast_translation_title']

	def item_link(self, obj):
		return reverse('blog:post_detail', kwargs={'pk': obj['pk'], 'slug': obj['fast_translation_slug']})

	def item_description(self, obj):
		return obj['fast_translation_summary']

	def item_author_name(self, obj):
		name = obj["author__username"]
		if name is None:
			return name
		full_name = (f'{obj["author__first_name"]} {obj["author__last_name"]}').strip()
		return full_name or name

	def item_pubdate(self, obj):
		return obj['pub_time']

	def item_updateddate(self, obj):
		return obj['date_updated']

	def item_categories(self, obj):
		category = self.category_translations.get(obj['category_id'])
		if category:
			return [category]
		else:
			return []


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
		obj = self.get_object()
		return super().get_context_data(object=obj, category=obj, **kwargs)


class UserBlogPostListView(BlogPostListView):
	def get_object(self):
		obj = getattr(self, 'object', None)
		if obj is None:
			obj = get_object_or_404(User, pk=self.kwargs['pk'])
			self.object = obj
		return obj

	def get_queryset(self):
		return super().get_queryset().filter(author=self.get_object())

	def get_context_data(self, **kwargs):
		return super().get_context_data(object=self.get_object(), **kwargs)


class BlogPostAttachmentsList(AttachmentListAndUploadView):
	model_class = BlogPost


class BlogPostDetailView(DetailView):
	QUERYSET = (BlogPost.objects
		.prefetch_category()
		.select_related('gallery', 'gallery__primary_attachment', 'author'))

	def get_queryset(self):
		return self.QUERYSET.published().fast_translate()
