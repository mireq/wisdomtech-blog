# -*- coding: utf-8 -*-
import logging

from utils.syntax_highlight import format_code


logger = logging.getLogger(__name__)


def process_content(content: str):
	if not content:
		return content

	from lxml import etree
	import lxml.html

	def replace_element(element, content):
		if callable(content):
			content = content(element)
		if not isinstance(content, str):
			content = etree.tostring(content, encoding='utf-8').decode('utf-8')
		code = f'<div>{content}</div>'
		subtree = None
		try:
			subtree = lxml.html.fromstring(code)
		except etree.ParserError:
			return
		previous = element.getprevious()
		if subtree.text is not None:
			if previous is not None:
				previous.tail = (previous.tail or '') + subtree.text
			else:
				parent = element.getparent()
				parent.text = (parent.text or '') + subtree.text
		for child in subtree.iterchildren():
			element.addprevious(child)
		element.drop_tree()

	def highlight_code(element, lang):
		content = etree.tostring(element, encoding='utf-8').decode('utf-8')
		tag_begin = content[:content.find('>')+1]
		tag_end = content[content.rfind('<'):]
		content[content.find('>')+1:content.rfind('<')]
		try:
			code = format_code(content, lang)
			return f'{tag_begin}{code}{tag_end}'
		except Exception:
			logger.exception("Failed to highlight code")
			return element

	try:
		tree = lxml.html.fromstring(content)
	except etree.ParserError:
		return content
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

	code = etree.tostring(tree, encoding='utf-8').decode('utf-8')
	return code[code.find('>')+1:code.rfind('<')]
