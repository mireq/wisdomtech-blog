# -*- coding: utf-8 -*-
from collections.abc import Collection, Mapping
from copy import deepcopy
from typing import Iterable, Union, Optional

from django.conf import settings
from django.utils.functional import Promise
from tinymce.widgets import TinyMCE


def recursive_map(val, fn):
	if isinstance(val, Mapping):
		return type(val)({k: recursive_map(v, fn) for k, v in val.items()})
	elif isinstance(val, Collection) and not isinstance(val, str) and not isinstance(val, Promise):
		return type(val)(recursive_map(v, fn) for v in val)
	else:
		return fn(val)


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
		self.mce_attrs['images_upload_handler'] = 'attachments_upload_handler'
		self.mce_attrs['images_upload_url'] = url

	def get_mce_config(self, *args, **kwargs):
		config = deepcopy(super().get_mce_config(*args, **kwargs))
		config = recursive_map(config, lambda v: str(v) if isinstance(v, Promise) else v)
		return config
