# -*- coding: utf-8 -*-
import base64
import hashlib
from uuid import uuid4


def hashed(source_filename, prepared_options, thumbnail_extension, **kwargs):
	output_format = kwargs.get('thumbnail_options', {}).get('output_format')
	if output_format:
		thumbnail_extension = f'{thumbnail_extension}.{output_format}'
		prepared_options = [opt for opt in prepared_options if opt != f'output_format-{output_format}']
	digest = hashlib.sha1(':'.join(prepared_options[1:]).encode('utf-8')).digest()
	safe_hash = base64.urlsafe_b64encode(digest[:(len(digest)//3)*3]).decode('utf-8')
	return '.'.join([source_filename, '_'.join(prepared_options[:1] + [safe_hash, str(uuid4())]), thumbnail_extension])
