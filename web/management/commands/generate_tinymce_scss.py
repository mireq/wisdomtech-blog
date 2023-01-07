# -*- coding: utf-8 -*-
from pathlib import Path

import sass
from django.contrib.staticfiles import finders
from django.core.management import BaseCommand


class Command(BaseCommand):
	def handle(self, *args, **options):
		src = finders.find('css/tinymce.scss')
		style_code = sass.compile(filename=src)
		output_filename = Path(src).parent / 'tinymce.css'
		with output_filename.open('w') as fp:
			fp.write(style_code)
