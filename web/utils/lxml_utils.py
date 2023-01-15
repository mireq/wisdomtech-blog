# -*- coding: utf-8 -*-
import logging
from typing import Union, Callable, Tuple

import lxml.html
from lxml import etree

from web.utils.syntax_highlight import format_code


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
		content = content(element)
	# if it's element, convert it to string
	if not isinstance(content, str):
		content = etree.tostring(content, encoding='utf-8').decode('utf-8')
	# wrap content (needed to correctly parse it)
	code = f'<div>{content}</div>'
	# parse code
	tree = None
	try:
		tree = lxml.html.fromstring(code)
	except etree.ParserError:
		return

	# insert text of tree
	previous = element.getprevious()
	if tree.text is not None:
		if previous is not None:
			previous.tail = (previous.tail or '') + tree.text
		else:
			parent = element.getparent()
			parent.text = (parent.text or '') + tree.text
	# and children
	for child in tree.iterchildren():
		element.addprevious(child)
	# drop old element
	element.drop_tree()


def highlight_code(element, lang):
	content = etree.tostring(element, encoding='utf-8').decode('utf-8')
	content, tag_begin, tag_end = unwrap_tag(content)
	try:
		code = format_code(content, lang)
		return f'{tag_begin}{code}{tag_end}'
	except Exception:
		logger.exception("Failed to highlight code")
		return element
