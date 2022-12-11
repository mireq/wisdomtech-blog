# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UsernameField
from django_attachments.models import Library
from parler.forms import TranslatableModelForm

from .models import User


class UserChangeForm(BaseUserChangeForm, TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'gallery' in self.fields:
			self.fields['gallery'].required = False

	def save(self, commit=True):
		obj = super().save(commit=False)
		if not hasattr(obj, 'gallery'):
			lib = Library()
			lib.save()
			obj.gallery = lib
		if commit:
			obj.save()
		return obj

	class Meta:
		model = User
		fields = ['subtitle', 'short_description', 'description', 'gallery']
		field_classes = {
			"username": UsernameField,
		}
