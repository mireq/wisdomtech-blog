# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from typing import Union, Callable, Tuple

import lxml.html
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django_attachments.models import Attachment
from lxml import etree

from web.utils.syntax_highlight import format_code
from web.utils.thumbnail.generator import generate_thumbnails


logger = logging.getLogger(__name__)


def unwrap_tag(content) -> Tuple[str, str, str]:
	"""
	Unwraps tag and returns content, start of tag and end of tag
	"""
	tag_begin = content[:content.find('>')+1]
	tag_end = content[content.rfind('<'):]
	return content[content.find('>')+1:content.rfind('<')], tag_begin, tag_end


def replace_element(element: etree.ElementBase, content: Union[etree.ElementBase, Callable, str]):
	# if it's callable, call it
	if callable(content):
		e = deepcopy(element)
		e.tail = ''
		content = content(e)
	# if it's element, convert it to string
	if not isinstance(content, str):
		content = etree.tostring(content, encoding='utf-8').decode('utf-8')

	fragments = lxml.html.fragments_fromstring(content)
	previous = element.getprevious()
	parent = element.getparent()

	for fragment in fragments:
		if isinstance(fragment, str):
			if previous is None:
				parent.text = (parent.text or '') + fragment
			else:
				parent.tail = (parent.tail or '') + fragment
		else:
			element.addprevious(fragment)
	element.drop_tree()


def highlight_code(element, lang):
	content = etree.tostring(element, encoding='utf-8', method='html').decode('utf-8')
	content, tag_begin, tag_end = unwrap_tag(content)
	try:
		code = format_code(content, lang)
		return f'{tag_begin}{code}{tag_end}'
	except Exception:
		logger.exception("Failed to highlight code")
		return element


def set_image_size(element, fp):
	img = Image.open(fp)
	size = img.size
	img.close()
	element.attrib['width'] = str(size[0])
	element.attrib['height'] = str(size[1])


def make_thumbnails(element):
	src = element.attrib['src']

	if not src.startswith(settings.MEDIA_URL):
		return element

	image_path = src[len(settings.MEDIA_URL):]
	try:
		with default_storage.open(image_path, 'rb') as fp:
			classes = element.attrib.get('class', '').split()

			try:
				set_image_size(element, fp)
			except Exception:
				logger.exception("Failed to set image size")
				return element

			if 'no-thumbnail' in classes:
				return element

			field = Attachment._meta.get_field('file')
			field_file = FieldFile(instance=None, field=field, name=image_path)
			field_file.file = fp

			thumbnails = generate_thumbnails(field_file, 'article')
			if not thumbnails:
				return element

			img_attrs = dict(element.attrib)
			first = thumbnails[0]

			original_size = None
			thumbnail_size = None
			try:
				original_size = default_storage.size(image_path)
				thumbnail_size = default_storage.size(first['name'])
			except NotADirectoryError:
				pass

			if original_size is not None and thumbnail_size is not None:
				if original_size < thumbnail_size:
					return element


			img_attrs['width'] = str(first['size'][0])
			img_attrs['height'] = str(first['size'][1])
			img_attrs['src'] = str(first['url'])
			img_attrs['loading'] = 'lazy'
			img_attrs['data-original-image'] = field_file.url

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
				img_attrs['srcset'] = img_srcs

			if webp_srcs:
				picture = lxml.etree.Element('picture')
				lxml.etree.SubElement(picture, 'source', {'type': 'image/webp', 'srcset': webp_srcs})
				lxml.etree.SubElement(picture, 'img', img_attrs)
				return picture
			else:
				return lxml.etree.Element('img', img_attrs)
	except Exception:
		logger.exception("Failed to generate thumbnails")
		return element

	return element


def wrap_table(element):
	wrapper = lxml.etree.Element('div')
	classes = ['table']
	if 'class' in element.attrib:
		classes.extend(element.attrib['class'].split())
		del element.attrib['class']
	wrapper.attrib['class'] = ' '.join(classes)
	wrapper.append(element)
	return wrapper
