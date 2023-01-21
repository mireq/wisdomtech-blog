# -*- coding: utf-8 -*-
import re
from typing import Tuple


HYPHENATE_TAGS_INCLUDE = {'p', 'td', 'th', 'figcaption', 'ul', 'ol', 'dl', 'blockquote'}
HYPHENATE_TAGS_EXCLUDE = {'code', 'pre'}
WORD_SPLIT_RX = re.compile(r'(\w+)')


def unwrap_tag(content) -> Tuple[str, str, str]:
	"""
	Unwraps tag and returns content, start of tag and end of tag
	"""
	tag_begin = content[:content.find('>')+1]
	tag_end = content[content.rfind('<'):]
	return content[content.find('>')+1:content.rfind('<')], tag_begin, tag_end


def hyphenate_text(text: str, dic):
	if dic is None:
		return text
	parts = WORD_SPLIT_RX.split(text)
	parts = [dic.inserted(part, hyphen='\u00AD') if WORD_SPLIT_RX.match(part) else part for part in parts]
	return ''.join(parts)


def process_content(content: str, language_code: str):
	if not content:
		return content

	from .lxml_utils import replace_element, highlight_code, make_thumbnails
	from lxml import etree
	import lxml.html
	import pyphen

	dictionaries = {}

	def get_dict(lang):
		if lang not in dictionaries:
			try:
				dictionaries[lang] = pyphen.Pyphen(lang=lang)
			except Exception:
				dictionaries[lang] = None
		return dictionaries[lang]

	fragments = lxml.html.fragments_fromstring(content)
	tree = lxml.html.Element('div')
	for fragment in fragments:
		if isinstance(fragment, str):
			tree.text = fragment
		else:
			tree.append(fragment)

	tag_stack = []
	lang_stack = [language_code]

	for action, element in etree.iterwalk(tree, events=['start', 'end']):
		if action == 'start':
			tag_stack.append(element.tag)
			if 'lang' in element.attrib:
				lang_stack.append(element.attrib['lang'])
			if (set(tag_stack).intersection(HYPHENATE_TAGS_INCLUDE)) and not (set(tag_stack).intersection(HYPHENATE_TAGS_EXCLUDE)) and element.text:
				element.text = hyphenate_text(element.text, get_dict(lang_stack[-1]))
		if action == 'end':
			tag_stack.pop()
			if 'lang' in element.attrib:
				lang_stack.pop()
		if (set(tag_stack).intersection(HYPHENATE_TAGS_INCLUDE)) and not (set(tag_stack).intersection(HYPHENATE_TAGS_EXCLUDE)) and element.tail:
			element.tail = hyphenate_text(element.tail, get_dict(lang_stack[-1]))
		if action == 'end':
			if element.tag == 'pre':
				cls = element.attrib.get('class', '').split()
				language = None
				for c in cls:
					if c.startswith('code-'):
						language = c[len('code-'):]
						break
				if language is not None:
					replace_element(element, lambda element, lang=language: highlight_code(element, lang))
			if element.tag == 'img' and 'src' in element.attrib:
				replace_element(element, make_thumbnails)

	code = etree.tostring(tree, encoding='utf-8', method='html').decode('utf-8')
	return unwrap_tag(code)[0]
