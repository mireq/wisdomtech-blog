# -*- coding: utf-8 -*-
import os
from collections import namedtuple
from copy import deepcopy

from django.conf import settings
from easy_thumbnails.files import get_thumbnailer


DEFAULT_SIZES = [1, 2]
DEFAULT_FORMATS = [None, 'webp']

ThumbnailInfo = namedtuple('ThumbnailInfo', ['thumbnail', 'url', 'size', 'size_hint', 'format'])


def get_thumbnail_alias_options(alias):
	return deepcopy(settings.THUMBNAIL_ALIASES[''][alias])


def generate_thumbnails(source, alias, sizes=None, size_attrs=None):
	if not source:
		return []

	thumbnail_options = get_thumbnail_alias_options(alias)
	if thumbnail_options.get('preserve_aspect') and thumbnail_options.get('size'):
		thumbnail_options['preserve_aspect'] = thumbnail_options['size']

	thumbnail_sizes = thumbnail_options.pop('sizes', None)
	thumbnail_size_attrs = thumbnail_options.pop('size_attrs', None)
	if sizes is None:
		sizes = thumbnail_sizes
	if size_attrs is None:
		size_attrs = thumbnail_size_attrs

	size_attrs = size_attrs or {}
	size_attrs_offset = 0
	sizes = DEFAULT_SIZES if sizes is None else sizes
	if not 1 in sizes:
		sizes = [1] + sizes
		size_attrs_offset = -1

	has_absolute = False

	formats = DEFAULT_FORMATS
	if thumbnail_options.get('alpha'):
		formats = [None]

	# preparing options
	thumbnails = {}
	for output_format in formats:
		for num, size in enumerate(sizes):
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
			num += size_attrs_offset
			if num >= 0:
				for attr_key, attr_list in size_attrs.items():
					if num < len(attr_list):
						opts[attr_key] = attr_list[num]
			thumbnails[(output_format, size)] = opts

	# index to remove duplicated images if source size is lower
	generated_images = set()
	has_alpha = False
	thumbnail_instances = []

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

		# check duplicates
		thumbnail_key = (output_format, thumbnail.width)
		# check presence, there can be a rounding error
		if thumbnail_key in generated_images:
			continue
		generated_images.add(thumbnail_key)

		thumbnail_instances.append(ThumbnailInfo(
			thumbnail,
			thumbnail.url,
			(thumbnail.width, thumbnail.height),
			f'{thumbnail.width}w' if has_absolute else f'{size}x',
			output_format,
		))

	return thumbnail_instances
