# -*- coding: utf-8 -*-
import os

from compressor.filters.css_default import CssAbsoluteFilter as BaseCssAbsoluteFilter


IGNORED_EXTENSIONS = {
	'.woff',
	'.woff2',
	'.ttf',
}


class CssAbsoluteFilter(BaseCssAbsoluteFilter):
	def add_suffix(self, url):
		ext = os.path.splitext(url)[1]
		if ext.lower() in IGNORED_EXTENSIONS:
			return url
		return super().add_suffix(url)
