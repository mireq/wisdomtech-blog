# -*- coding: utf-8 -*-
from django.contrib import admin
from django_attachments.admin import AttachmentsAdminMixin
from parler.admin import TranslatableAdmin

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostAdmin(AttachmentsAdminMixin, TranslatableAdmin, admin.ModelAdmin):
	form = BlogPostForm
	list_display = ['get_title', 'is_published', 'author']
	list_filter = ['author']

	def save_form(self, request, form, change):
		obj = super().save_form(request, form, change)
		if not hasattr(obj, 'author'):
			obj.author = request.user
		return obj

	def get_queryset(self, request):
		return super().get_queryset(request).fast_translate(fallback=True).select_related('author')

	def get_title(self, obj):
		return obj.fast_translation_getter('title')
	get_title.admin_order_field = 'fast_translation_title'


admin.site.register(BlogPost, BlogPostAdmin)
