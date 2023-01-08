# -*- coding: utf-8 -*-
from typing import Iterable, Union, Optional

from django.conf import settings
from tinymce.widgets import TinyMCE


class RichTextWidget(TinyMCE):
	edit_url = None

	def __init__(self, *args, config: Optional[Union[str, Iterable]], **kwargs):
		mce_attrs = None

		if config is not None: # Allow cusotm configuration using TINYMCE_CONFIGS
			configs = getattr(settings, 'TINYMCE_CONFIGS', {})
			# It's just string
			if isinstance(config, str):
				mce_attrs = configs.get(config)
			# of list of configs
			else:
				mce_attrs = {}
				for name in config:
					mce_attrs.update(configs.get(name, {}))

		super().__init__(*args, mce_attrs=mce_attrs, **kwargs)

	def set_edit_url(self, url: str):
		self.edit_url = url
		self.attrs['edit_url'] = url
		self.mce_attrs['file_picker_callback'] = 'attachments_filebrowser'
		self.mce_attrs['images_upload_url'] = url
