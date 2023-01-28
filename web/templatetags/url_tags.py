# -*- coding: utf-8 -*-
from django_jinja import library
from jinja2 import pass_context


def is_absolute(url):
	return url.startswith('http://') or url.startswith('https://') or url.startswith('//')


def build_absolute_uri(ctx, url):
	if is_absolute(url):
		return url
	return ctx['request'].build_absolute_uri(url)


library.filter(pass_context(build_absolute_uri))
