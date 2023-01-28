# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UsernameField
from django.urls import reverse
from django_attachments.models import Library
from parler.forms import TranslatableModelForm

from .models import User
from web.utils.widgets import RichTextWidget


class UserChangeForm(BaseUserChangeForm, TranslatableModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'gallery' in self.fields:
			self.fields['gallery'].required = False
		if self.instance and self.instance.pk:
			url = reverse('accounts:user_attachments', kwargs={'pk': self.instance.pk})
			self.fields['description'].widget.set_edit_url(url)

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
		widgets = {
			'short_description': RichTextWidget(config='basic'),
			'description': RichTextWidget(config='content'),
		}
