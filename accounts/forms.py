# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UsernameField
from parler.forms import TranslatableModelForm

from .models import User


class UserChangeForm(BaseUserChangeForm, TranslatableModelForm):
	class Meta:
		model = User
		fields = ['subtitle', 'short_description', 'description']
		field_classes = {
			"username": UsernameField,
		}
