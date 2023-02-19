# -*- coding: utf-8 -*-
import weakref

import jinja2.exceptions
from django.utils.functional import cached_property


class Environment(jinja2.Environment):
	@cached_property
	def _loader_ref(self):
		if self.loader is None:
			raise TypeError("no loader for this environment specified")
		return weakref.ref(self.loader)

	def _load_template(self, name, globals): # pylint: disable=redefined-builtin
		if self.loader is None:
			raise TypeError("no loader for this environment specified")
		cache_key = (weakref.ref(self.loader), name)
		if self.cache is not None:
			template = self.cache.get(cache_key)
			if template is not None and (not self.auto_reload or template.is_up_to_date):
				if template == '':
					raise jinja2.exceptions.TemplateNotFound(name)
				if globals:
					template.globals.update(globals)
				return template
		try:
			template = self.loader.load(self, name, self.make_globals(globals))
		except jinja2.exceptions.TemplateNotFound:
			if self.cache is not None and not self.auto_reload:
				self.cache[cache_key] = ''
			raise

		if self.cache is not None:
			self.cache[cache_key] = template
		return template
