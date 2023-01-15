# -*- coding: utf-8 -*-
from typing import Tuple


def unwrap_tag(content) -> Tuple[str, str, str]:
	"""
	Unwraps tag and returns content, start of tag and end of tag
	"""
	tag_begin = content[:content.find('>')+1]
	tag_end = content[content.rfind('<'):]
	return content[content.find('>')+1:content.rfind('<')], tag_begin, tag_end


def process_content(content: str):
	if not content:
		return content

	from .lxml_utils import replace_element, highlight_code, make_thumbnails
	from lxml import etree
	import lxml.html

	fragments = lxml.html.fragments_fromstring(content)
	tree = lxml.html.Element('div')
	for fragment in fragments:
		if isinstance(fragment, str):
			tree.text = fragment
		else:
			tree.append(fragment)

	for action, element in etree.iterwalk(tree):
		if element.tag == 'pre' and action == 'end':
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
