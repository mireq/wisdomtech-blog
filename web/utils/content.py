# -*- coding: utf-8 -*-
def process_content(content: str):
	if not content:
		return content

	from lxml import etree
	import lxml.html

	def replace_element(element, content):
		if callable(content):
			content = content(element)
		if isinstance(content, str):
			code = f'<div>{content}</div>'
			subtree = None
			try:
				subtree = lxml.html.fromstring(code)
			except etree.ParserError:
				return
		else:
			subtree = content
		previous = element.getprevious()
		if subtree.text is not None:
			if previous is not None:
				previous.tail = (previous.tail or '') + subtree.text
			else:
				parent = element.getparent()
				parent.text = (parent.text or '') + subtree.text
		for child in subtree.iterchildren():
			element.addprevious(child)
		print(element)
		element.drop_tree()

	def highlight_code(element, lang):
		return "ook"

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
					language = cls[len('code-'):]
					break
			if language is not None:
				replace_element(element, lambda element, lang=language: highlight_code(element, lang))

	code = etree.tostring(tree, encoding='utf-8').decode('utf-8')
	return code[code.find('>')+1:code.rfind('<')]
