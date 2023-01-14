# -*- coding: utf-8 -*-
from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
	name = 'blog'
	verbose_name = _("Blog")

	def ready(self):
		from .signals import handlers # pylint: disable=unused-import
