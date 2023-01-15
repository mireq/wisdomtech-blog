# -*- coding: utf-8 -*-
from django_jinja import library


def translate_field(obj, field):
	return obj.fast_translation_getter(field)


library.filter(translate_field)
