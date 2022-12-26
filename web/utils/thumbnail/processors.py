# -*- coding: utf-8 -*-
from PIL import Image, ImageColor


def alpha(im, alpha=None, output_format=None, **kwargs):
	"""
	Controls alpha channel and output format.

	If ``alpha`` is True - alpha will be preserved. To remove channel,
	``alpha`` should be ``False``.

	Argument ``output_format`` is used to force format, like (`jpeg` or `webp`).
	"""
	if alpha is False or output_format == 'webp':
		if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
			background = kwargs.get('background')
			if background:
				bg_image = Image.new('RGBA', im.size, ImageColor.getrgb(background))
				if im.mode != 'RGBA':
					im = im.convert('RGBA')
				im = Image.alpha_composite(bg_image, im).convert('RGB')
			else:
				im = im.convert('RGB')
	elif alpha is True:
		if im.mode != 'RGBA':
			im = im.convert('RGBA')
	return im
