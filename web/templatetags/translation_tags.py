# -*- coding: utf-8 -*-
from django_jinja import library


def translated_field(obj, field):
	return obj.fast_translation_getter(field)


library.filter(translated_field)
