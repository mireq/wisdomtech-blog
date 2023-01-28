# -*- coding: utf-8 -*-
import json
from hashlib import md5

from django.conf import settings
from django.core.cache import caches
from django.utils.html import escape as escape_html, format_html
from django.utils.safestring import mark_safe
from django_jinja import library

from web.utils.thumbnail.generator import generate_thumbnails


CACHE_NAME = getattr(settings, 'THUMBNAIL_CACHE', None)
USE_CACHE = bool(CACHE_NAME)
CACHE_PREFIX = getattr(settings, 'THUMBNAIL_CACHE_PREFIX', 'tmb_')


def generate_thumbnails_cached(source, alias):
	if USE_CACHE:
		key = CACHE_PREFIX + md5(json.dumps([str(source), alias]).encode('utf-8')).hexdigest()
		thumbnails = caches[CACHE_NAME].get(key)
		if thumbnails is None:
			thumbnails = generate_thumbnails(source, alias)
			caches[CACHE_NAME].set(key, thumbnails, timeout=3600)
	else:
		thumbnails = generate_thumbnails(source, alias)
	return thumbnails


def thumbnail_tag(source, alias, attrs=None, only_data=False):
	thumbnails = generate_thumbnails_cached(source, alias)

	if not thumbnails:
		return ''

	first = thumbnails[0]

	if isinstance(attrs, dict):
		attrs = attrs.copy()
		attrs.setdefault('width', str(first['size'][0]))
		attrs.setdefault('height', str(first['size'][1]))
		attrs = [f'{escape_html(key)}="{escape_html(val)}"' for key, val in attrs.items()]
		attrs = ' '.join(attrs)
	attrs = mark_safe(' ' + attrs if attrs else '')

	img_srcs = []
	webp_srcs = []

	for thumbnail in thumbnails:
		if thumbnail['format'] == 'webp':
			webp_srcs.append(f'{thumbnail["url"]} {thumbnail["size_hint"]}')
		else:
			img_srcs.append(f'{thumbnail["url"]} {thumbnail["size_hint"]}')

	webp_srcs = ', '.join(webp_srcs)
	img_srcs = ', '.join(img_srcs)
	if img_srcs:
		img_srcs = format_html(' srcset="{}"', img_srcs)
	img_src = first['url']

	if only_data:
		return thumbnails

	if webp_srcs:
		return format_html('<picture><source type="image/webp" srcset="{}"><img src="{}"{}{}></picture>', webp_srcs, img_src, img_srcs, attrs)
	else:
		return format_html('<img src="{}"{}{}>', img_src, img_srcs, attrs)


library.global_function(thumbnail_tag)
