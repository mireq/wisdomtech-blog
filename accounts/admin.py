# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django_attachments.admin import AttachmentsAdminMixin
from parler.admin import TranslatableAdmin

from . import views
from .forms import UserChangeForm
from .models import User


class UserAdmin(AttachmentsAdminMixin, TranslatableAdmin, BaseUserAdmin):
	form = UserChangeForm

	def get_fieldsets(self, request, obj=None):
		fieldsets = super().get_fieldsets(request, obj)
		if obj:
			fieldsets += (
				(_("Info"), {'fields': ('subtitle', 'short_description', 'description',)}),
				(_("SEO"), {'fields': ('page_title', "meta_description"), 'classes': ('collapse',)}),
				(_("Files"), {'fields': ('gallery',)}),
			)
		return fieldsets

	def get_urls(self):
		urls = super().get_urls()
		attachments = [path('<int:pk>/attachments/', views.UserAttachmentsList.as_view(), name='accounts_user_attachments')]
		return attachments + urls


admin.site.register(User, UserAdmin)
