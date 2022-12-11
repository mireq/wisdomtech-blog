# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from parler.admin import TranslatableAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm
from .models import User


#class UserAdmin(TranslatableAdmin, BaseUserAdmin):
#	form = UserChangeForm
class UserAdmin(TranslatableAdmin, BaseUserAdmin):
	form = UserChangeForm

	def get_fieldsets(self, request, obj=None):
		fieldsets = super().get_fieldsets(request, obj)
		if obj:
			fieldsets += (
				(_('Info'), {'fields': ['subtitle', 'short_description', 'description']}),
			)
		return fieldsets


admin.site.register(User, UserAdmin)
