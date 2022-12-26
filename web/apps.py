# -*- coding: utf-8 -*-
import re

from django.apps import AppConfig as BaseAppConfig
from django.db import models
from django.conf import settings


IGNORED_DECONSTRUCT_ATTRS = {'verbose_name', 'help_text', 'error_messages'}


class AppConfig(BaseAppConfig):
	name = 'web'
	verbose_name = 'web'

	def ready(self):
		self.patch_migrations()
		self.patch_deconstruct()
		self.patch_model_bakery()

	def patch_migrations(self):
		from django.db.migrations.writer import MigrationWriter
		rx = re.compile('^(    )+', flags=re.MULTILINE)
		replace = lambda match: '\t'*(len(match.group())//4)
		old_as_string = MigrationWriter.as_string
		MigrationWriter.as_string = lambda self: rx.sub(replace, old_as_string(self))

	def patch_deconstruct(self):
		original_deconstruct = models.Field.deconstruct
		def new_deconstruct(self):
			name, path, args, kwargs = original_deconstruct(self)
			kwargs = {key: value for key, value in kwargs.items() if key not in IGNORED_DECONSTRUCT_ATTRS}
			return name, path, args, kwargs
		models.Field.deconstruct = new_deconstruct

	def patch_model_bakery(self):
		if settings.CURRENT_COMMAND != 'test':
			return
		from model_bakery import baker, random_gen
		baker.generators.add('django_attachments.fields.GalleryField', random_gen.gen_related)
