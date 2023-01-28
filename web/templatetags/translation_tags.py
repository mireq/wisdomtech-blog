# -*- coding: utf-8 -*-
from django_jinja import library
from django.urls import reverse
from django.utils import translation


def translated_field(obj, field):
	return obj.fast_translation_getter(field)


def translated_url(language_code, urlpattern, *args, **kwargs):
	with translation.override(language_code):
		return reverse(urlpattern, args=args, kwargs=kwargs)


library.filter(translated_field)
library.global_function(translated_url)
