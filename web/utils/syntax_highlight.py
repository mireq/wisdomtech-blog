#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import operator
import re
import sys
from builtins import chr as chr_
from collections import namedtuple
from html.entities import entitydefs
from io import StringIO, BytesIO

from django.template.defaultfilters import striptags
from django.utils.encoding import force_str
from lxml import etree


logger = logging.getLogger(__name__)


LEXERS = {}


ENTITY_PATTERN = re.compile(r'&(\w+?);')
DECIMAL_ENTITY_PATTERN = re.compile(r'&\#(\d+?);')

AdditionalTag = namedtuple('AdditionalTag', ['action', 'pos', 'elem', 'text'])
pattern = re.compile(r'&(\w+?);')
dec_pattern = re.compile(r'&\#(\d+?);')


def html_entity_decode_char(m, defs=None):
	defs = defs or entitydefs
	try:
		return force_str(defs[m.group(1)], errors='replace')
	except KeyError:
		return m.group(0)


def xml_entity_decode_char(m):
	try:
		return chr_(int(m.group(1)))
	except (UnicodeError, ValueError):
		return m


def html_entity_decode(string):
	without_entity = ENTITY_PATTERN.sub(html_entity_decode_char, string)
	return DECIMAL_ENTITY_PATTERN.sub(xml_entity_decode_char, without_entity)


def html_split_text_and_tags(code):
	try:
		# Strip new lines
		code = code.splitlines()
		while code and not code[0].strip():
			code.pop(0)
		while code and not code[-1].strip():
			code.pop()
		code = '\n'.join(code)

		# Tax found in code
		additional_tags = []
		fp = BytesIO(f'<pre>{code}</pre>'.encode('utf-8'))
		text = StringIO()

		# Don't export html / body / pre
		ignore_tags = {'html', 'body', 'pre'}

		# Split content to plain text and tags
		context = etree.iterparse(fp, events=('start', 'end'), html=True, remove_comments=True, remove_pis=True)
		for action, elem in context:

			if elem.tag.lower() == 'br':
				if action == 'end':
					text.write('\n')
					text.write(elem.tail or '')
					elem.clear()
				continue

			if action == 'start':
				if elem.tag not in ignore_tags:
					additional_tags.append(AdditionalTag(action, text.tell(), elem, elem.text))
				text.write(elem.text or '')

			if action == 'end':
				if elem.tag not in ignore_tags:
					additional_tags.append(AdditionalTag(action, text.tell(), elem, elem.text))
				text.write(elem.tail or '')
				elem.clear()

		text = text.getvalue().rstrip('\n')
		if text:
			text = text + '\n'

		return text, additional_tags
	except Exception:
		logger.exception("Cannot parse code block")
		code = html_entity_decode(striptags(code))
		return code, []


class HtmlMarkupMerge(object):
	def __init__(self):
		# current element path
		self.element_stack = []
		self.element_context_stack = []
		self.additional_tags = []
		# position in code
		self.text_pos = 0
		# index of next additional tag
		self.next_additional_tag_index = 0
		self.xf = None

	def join(self, code, additional_tags):
		"""
		Join code with additional tags (and solving tag crossing)
		"""
		# clear status
		self.element_stack = []
		self.element_context_stack = []
		self.additional_tags = additional_tags
		self.text_pos = 0
		self.next_additional_tag_index = 0
		self.xf = None
		try:
			return self.perform_join(code)
		except Exception:
			logger.exception("Cannot merge code blocks")
			return code

	def perform_join(self, code):
		out = BytesIO()
		with etree.xmlfile(out, encoding='utf-8') as xf:
			self.xf = xf
			fp = BytesIO(f'<pre>{code}</pre>'.encode('utf-8'))
			ignore_tags = {'html', 'body'}
			context = etree.iterparse(fp, events=('start', 'end'), html=True, remove_comments=True, remove_pis=True)

			for action, elem in context:

				if elem.tag in ignore_tags: # Don't include html / body
					continue

				if action == 'start':
					self.push_tag(elem)
					self.write_text(elem.text)

				if action == 'end':
					self.pop_tag(elem)
					self.write_text(elem.tail)

		html_output = out.getvalue().decode('utf-8')[5:-6]
		if html_output and html_output[-1] == '\n':
			html_output = html_output[:-1]
		return html_output

	def push_tag(self, elem):
		elem_context = self.xf.element(elem.tag, **dict(elem.attrib))
		elem_context.__enter__()
		self.element_stack.append(elem)
		self.element_context_stack.append(elem_context)

	def pop_tag(self, elem):
		# find index of element to remove
		idx = len(self.element_stack) - operator.indexOf(reversed(self.element_stack), elem) - 1
		# close crossing elements
		close_count = len(self.element_stack) - idx
		cross_removed_elements = []
		for i in range(close_count):
			context_element = self.element_context_stack.pop()
			element = self.element_stack.pop()
			if i < close_count - 1:
				cross_removed_elements.append(element)
			context_element.__exit__(None, None, None)
		# open closed elements
		for el in reversed(cross_removed_elements):
			self.push_tag(el)

	def write_text(self, text):
		while text:
			start_index = self.text_pos
			end_index = start_index + len(text)
			next_tag = None
			if self.next_additional_tag_index < len(self.additional_tags):
				next_tag = self.additional_tags[self.next_additional_tag_index]
			if next_tag is None or next_tag.pos > end_index:
				self.xf.write(text)
				self.text_pos += len(text)
				text = ''
			else:
				begin, text = text[:next_tag.pos - start_index], text[next_tag.pos - start_index:]
				self.xf.write(begin)
				self.text_pos += len(begin)
				self.next_additional_tag_index += 1
				if next_tag.action == 'start' and next_tag.text is None:
					self.xf.write(next_tag.elem)
				else:
					if next_tag.action == 'start':
						self.push_tag(next_tag.elem)
					elif next_tag.action == 'end':
						self.pop_tag(next_tag.elem)


def format_code(code, lang):
	import pygments
	from pygments import lexers, formatters, util

	if not LEXERS:
		for lex in pygments.lexers.get_all_lexers():
			for shortcut in lex[1]:
				LEXERS[shortcut] = lex[0]

	if not lang in LEXERS:
		return None

	if len(code) > 200000:
		return None

	code, additional_tags = html_split_text_and_tags(code)

	try:
		lexer = lexers.get_lexer_by_name(lang)
	except util.ClassNotFound:
		return None

	formatter = formatters.get_formatter_by_name('html')
	formatter.nowrap = True

	highlighted_code = pygments.highlight(code, lexer, formatter)
	if not additional_tags:
		return highlighted_code

	return HtmlMarkupMerge().join(highlighted_code, additional_tags)


def highlight_block(match):
	lang = match.group(2)
	pre_block_code = match.group(3)
	code = format_code(pre_block_code, lang)
	if code is None:
		return ''.join((match.group(1), pre_block_code, match.group(4)))
	else:
		return match.group(1) + code + match.group(4)


def highlight_pre_blocks(html):
	return re.sub(r'(<pre\s+class="code-([^"]+)">)(.*?)(</\s*pre>)', highlight_block, html, flags=re.DOTALL)


def main():
	content = sys.stdin.read()
	sys.stdout.write(highlight_pre_blocks(content))


if __name__ == "__main__":
	main()
