# -*- coding: utf-8 -*-
import jinja2.ext
from django.core.management.commands import makemessages
from django.template import engines
from django.utils.translation import template as trans_real
from django_jinja.backend import Jinja2


if jinja2.__version__.split('.')[0] == '2':
	jinja2.ext.GETTEXT_FUNCTIONS += ('pgettext', 'npgettext')

class Command(makemessages.Command):
	def handle(self, *args, **options):
		old_templatize = trans_real.templatize

		engine = None
		for template_engine in engines.all():
			if isinstance(template_engine, Jinja2):
				engine = template_engine

		def my_templatize(src, origin=None, **kwargs):
			try:
				translations = engine.env.extract_translations(src, gettext_functions=jinja2.ext.GETTEXT_FUNCTIONS)
			except Exception:
				return old_templatize(src, origin, **kwargs)
			new_text = ['' for __ in src.splitlines()]
			for translation in translations:
				lineno, fn, arguments = translation
				if isinstance(arguments, str):
					arguments = [arguments]
				new_text[lineno - 1] += '{}({})'.format(fn, ', '.join("'{}'".format(str(arg).replace('\n', '\\n').replace("'", "\\'")) for arg in arguments))
			return '\n'.join(new_text)

		trans_real.templatize = my_templatize

		super().handle(*args, **options)
