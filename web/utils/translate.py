# -*- coding: utf-8 -*-
import requests


def translate_google(content, target_language="auto", source_language="auto"):
	data = {
		'hl': target_language,
		'sl': source_language,
		'q': content,
		'ie':'UTF-8'
	}
	headers = {
		'User-Agent': 'Mozilla/5.0'
	}
	result = requests.get('http://translate.google.com/m', params=data, headers=headers)
	result.raise_for_status()
	print(result.text)
