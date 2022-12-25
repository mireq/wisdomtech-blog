# -*- coding: utf-8 -*-
from django.contrib import admin
from django_attachments.admin import AttachmentsAdminMixin
from parler.admin import TranslatableAdmin

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostAdmin(AttachmentsAdminMixin, TranslatableAdmin, admin.ModelAdmin):
	form = BlogPostForm

	def save_form(self, request, form, change):
		obj = super().save_form(request, form, change)
		if not hasattr(obj, 'author'):
			obj.author = request.user
		return obj

	def get_queryset(self, request):
		return super().get_queryset(request).fast_translate(fallback=True).select_related('author')


admin.site.register(BlogPost, BlogPostAdmin)
