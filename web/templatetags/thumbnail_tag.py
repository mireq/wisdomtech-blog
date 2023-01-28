# -*- coding: utf-8 -*-
from django.utils.html import escape as escape_html, format_html
from django.utils.safestring import mark_safe
from django_jinja import library

from web.utils.thumbnail.generator import generate_thumbnails


def thumbnail_tag(source, alias, attrs=None):
	thumbnails = generate_thumbnails(source, alias)
	if not thumbnails:
		return ''

	first = thumbnails[0]

	if isinstance(attrs, dict):
		attrs = attrs.copy()
		attrs.setdefault('width', str(first.size[0]))
		attrs.setdefault('height', str(first.size[1]))
		attrs = [f'{escape_html(key)}="{escape_html(val)}"' for key, val in attrs.items()]
		attrs = ' '.join(attrs)
	attrs = mark_safe(' ' + attrs if attrs else '')

	img_srcs = []
	webp_srcs = []

	for thumbnail in thumbnails:
		if thumbnail.format == 'webp':
			webp_srcs.append(f'{thumbnail.url} {thumbnail.size_hint}')
		else:
			img_srcs.append(f'{thumbnail.url} {thumbnail.size_hint}')

	webp_srcs = ', '.join(webp_srcs)
	img_srcs = ', '.join(img_srcs)
	if img_srcs:
		img_srcs = format_html(' srcset="{}"', img_srcs)
	img_src = first.url

	if webp_srcs:
		return format_html('<picture><source type="image/webp" srcset="{}"><img src="{}"{}{}></picture>', webp_srcs, img_src, img_srcs, attrs)
	else:
		return format_html('<img src="{}"{}{}>', img_src, img_srcs, attrs)


library.global_function(thumbnail_tag)
