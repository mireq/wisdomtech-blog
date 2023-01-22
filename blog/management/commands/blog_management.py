# -*- coding: utf-8 -*-
import logging

from django.core.management import BaseCommand, CommandParser

from ...models import BlogPost
from web.utils.content import process_content, count_words


BlogPostTranslation = BlogPost._parler_meta.root_model
logger = logging.getLogger(__name__)


class Command(BaseCommand):
	def add_arguments(self, parser):
		cmd = self

		class SubParser(CommandParser):
			def __init__(self, **kwargs):
				kwargs['called_from_command_line'] = getattr(cmd, "_called_from_command_line", None)
				super().__init__(**kwargs)

		subparsers = parser.add_subparsers(help="Command", dest='subcommand', required=True, parser_class=SubParser)
		subparsers.add_parser('preprocess_content', help="Preprocess content")

	def handle(self, *args, **options):
		subcommand = options['subcommand']
		return getattr(self, subcommand)(*args, **options)

	def preprocess_content(self, *args, **kwargs):
		for trans in BlogPostTranslation.objects.all():
			old_content = trans.processed_content
			try:
				new_content = process_content(trans.content, trans.language_code)
				new_words = count_words(trans.content)
			except Exception:
				logger.exception("Content cannot be processed")
				continue
			if old_content != new_content or trans.words != new_words:
				(BlogPostTranslation.objects
					.filter(pk=trans.pk)
					.update(processed_content=new_content, words=new_words))
