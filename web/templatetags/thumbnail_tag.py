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


def thumbnail_tag(source, alias, attrs=None, sizes=None):
	if not source:
		return ''

	thumbnail_options = get_thumbnail_alias_options(alias)

	if isinstance(attrs, dict):
		attrs = [f'{escape_html(key)}="{escape_html(val)}"' for key, val in attrs.items()]
		attrs = ' '.join(attrs)
	attrs = mark_safe(' ' + attrs if attrs else '')

	sizes = DEFAULT_SIZES if sizes is None else sizes
	if not 1 in sizes:
		sizes = [1] + sizes

	has_absolute = False

	formats = DEFAULT_FORMATS
	if thumbnail_options.get('alpha'):
		formats = [None]

	# preparing options
	thumbnails = {}
	for output_format in formats:
		for size in sizes:
			is_absolute = False
			try:
				size = int(size)
			except ValueError:
				if size.endswith('px'):
					is_absolute = True
					try:
						size = int(size[:-2])
					except ValueError:
						raise RuntimeError("Invalid size")
				else:
					raise RuntimeError("Invalid size")
			opts = thumbnail_options.copy()
			if output_format is not None:
				opts['output_format'] = output_format
			if is_absolute:
				opts['size'] = (size, int(size / opts['size'][0] * opts['size'][1]))
				has_absolute = True
			else:
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
		if has_absolute:
			size_hint = f'{thumbnail.width}w'
		else:
			size_hint = f'{size}x'
		if output_format == 'webp':
			webp_srcs.append(f'{thumbnail.url} {size_hint}')
		else:
			img_srcs.append(f'{thumbnail.url} {size_hint}')

	webp_srcs = ', '.join(webp_srcs)
	img_srcs = ', '.join(img_srcs)
	if img_srcs:
		img_srcs = format_html(' srcset="{}"', img_srcs)

	if webp_srcs:
		return format_html('<picture><source type="image/webp" srcset="{}"><img src="{}"{}{}></picture>', webp_srcs, img_src, img_srcs, attrs)
	else:
		return format_html('<img src="{}"{}{}>', img_src, img_srcs, attrs)



library.global_function(thumbnail_tag)
