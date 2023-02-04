# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models import F
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django_attachments.admin import AttachmentsAdminMixin
from parler.admin import TranslatableAdmin

from . import views
from .forms import BlogCategoryForm, BlogTagForm, BlogPostForm
from .models import BlogCategory, BlogTag, BlogPost


class BlogCategoryAdmin(TranslatableAdmin, admin.ModelAdmin):
	form = BlogCategoryForm
	search_fields = ['fast_translation_title']
	fieldsets = (
		(None, {'fields': ('title', 'slug',)}),
		(_("SEO"), {'fields': ('page_title', "meta_description"), 'classes': ('collapse',)}),
	)

	def get_queryset(self, request):
		return super().get_queryset(request).fast_translate(fallback=True)


class BlogTagAdmin(TranslatableAdmin, admin.ModelAdmin):
	form = BlogTagForm
	search_fields = ['fast_translation_title']

	def get_queryset(self, request):
		return super().get_queryset(request).fast_translate(fallback=True)


class BlogPostAdmin(AttachmentsAdminMixin, TranslatableAdmin, admin.ModelAdmin):
	form = BlogPostForm
	list_display = ['get_title', 'is_published', 'pub_time', 'author']
	list_filter = ['author', 'category', 'pub_time']
	raw_id_fields = ['author']
	search_fields = ['fast_translation_title']
	fieldsets = (
		(None, {'fields': ('title', 'slug', ('pub_time', 'is_published'), 'author', 'category', 'blog_tags', 'summary', 'perex', 'content')}),
		(_("Files"), {'fields': ('gallery', 'attachments')}),
		(_("SEO"), {'fields': ('page_title', "meta_description"), 'classes': ('collapse',)}),
	)

	def save_form(self, request, form, change):
		obj = super().save_form(request, form, change)
		if not hasattr(obj, 'author'):
			obj.author = request.user
		return obj

	def get_queryset(self, request):
		return (super().get_queryset(request)
			.fast_translate(fallback=True)
			.select_related('author'))

	def get_ordering(self, request):
		ordering = super().get_ordering(request)
		if not ordering:
			return (F('pub_time').desc(nulls_first=True), '-id')
		return ordering

	def get_title(self, obj):
		return obj.fast_translation_getter('title')
	get_title.admin_order_field = 'fast_translation_title'
	get_title.short_description = _("Title")

	def get_urls(self):
		urls = super().get_urls()
		attachments = [path('<int:pk>/attachments/', views.BlogPostAttachmentsList.as_view(), name='blog_blogpost_attachments')]
		return attachments + urls


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogTag, BlogTagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
