# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from django.conf import settings
from django.utils.html import escape as escape_html, format_html
from django.utils.safestring import mark_safe
from django_jinja import library
from easy_thumbnails.files import get_thumbnailer


DEFAULT_SIZES = [1, 2]
DEFAULT_FORMATS = [None, 'webp']


def get_thumbnail_alias_options(alias):
	return deepcopy(settings.THUMBNAIL_ALIASES[''][alias])


def thumbnail_tag(source, alias, attrs=None):
	if not source:
		return ''

	thumbnail_options = get_thumbnail_alias_options(alias)

	if isinstance(attrs, dict):
		attrs = [f'{escape_html(key)}="{escape_html(val)}"' for key, val in attrs.items()]
		attrs = ' '.join(attrs)
	attrs = mark_safe(' ' + attrs if attrs else '')

	sizes = DEFAULT_SIZES
	formats = DEFAULT_FORMATS
	if thumbnail_options.get('alpha'):
		formats = [None]

	# preparing options
	thumbnails = {}
	for output_format in formats:
		for size in sizes:
			opts = thumbnail_options.copy()
			if output_format is not None:
				opts['output_format'] = output_format
			opts['size'] = (opts['size'][0] * size, opts['size'][1] * size)
			thumbnails[(output_format, size)] = opts

	webp_srcs = []
	img_srcs = []
	img_src = ''
	has_alpha = False

	for props, options in thumbnails.items():
		output_format, size = props
		if output_format == 'webp' and has_alpha:
			continue

		thumbnail = get_thumbnailer(source).get_thumbnail(options)
		if not thumbnail:
			continue
		__, ext = os.path.splitext(thumbnail.name)
		if ext == '.png':
			has_alpha = True
		if output_format is None and size == 1:
			img_src = thumbnail.url
		elif output_format == 'webp':
			webp_srcs.append(thumbnail.url if size == 1 else f'{thumbnail.url} {size}x')
		else:
			img_srcs.append(f'{thumbnail.url} {size}x')

	webp_srcs = ', '.join(webp_srcs)
	img_srcs = ', '.join(img_srcs)
	if img_srcs:
		img_srcs = format_html(' srcset="{}"', img_srcs)

	if webp_srcs:
		return format_html('<picture><source type="image/webp" srcset="{}"><img src="{}"{}{}></picture>', webp_srcs, img_src, img_srcs, attrs)
	else:
		return format_html('<img src="{}"{}{}>', img_src, img_srcs, attrs)



library.global_function(thumbnail_tag)
