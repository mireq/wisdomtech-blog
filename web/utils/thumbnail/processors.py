# -*- coding: utf-8 -*-
import re
from dataclasses import dataclass
from fractions import Fraction
from math import floor, ceil
from typing import Tuple, Union, Optional

from PIL import Image


@dataclass
class CropOp:
	bbox: Tuple[int, int, int, int]
	resize: Optional[Tuple[int, int]]
	size: Tuple[int, int]


def calc_scale_and_crop(
	im: Image,
	size: Tuple[int, int],
	crop: Union[bool, str] = False,
	upscale: bool = None,
	zoom: Optional[float] = None,
	target: Optional[Union[Tuple[int, int], str]] = None
) -> CropOp:

	requested_x, requested_y = size
	source_x, source_y = im.size
	requested_aspect = Fraction(requested_x, requested_y)
	resize = None

	# calculate scale
	scale = (Fraction(requested_x, source_x), Fraction(requested_y, source_y))
	scale = max(scale) if crop else min(scale)
	if zoom is not None:
		scale *= (100 + zoom) / 100

	# limit scale if upscale is prohibited
	if scale > 1 and not upscale:
		scale = Fraction(1, 1)

	# resize image (always try ceil to later prefer x size)
	resize = (ceil(source_x * scale), ceil(source_y * scale))
	source_x, source_y = resize
	if resize == im.size:
		resize = None

	bbox = (0, 0, source_x, source_y)

	if crop:
		scale = max(Fraction(requested_x, source_x), Fraction(requested_y, source_y))

		result_x = floor(min(requested_x, (requested_x / scale)))
		result_y = floor(min(requested_y, (requested_y / scale)))

		if isinstance(target, str):
			target = re.match(r'(\d+)?,(\d+)?$', target)
			if target:
				target = target.groups()
		if target:
			focal_point = [int(n) if (n or n == 0) else 50 for n in target]
		else:
			focal_point = 50, 50

		focal_point_x = Fraction(source_x * focal_point[0], 100)
		focal_point_y = Fraction(source_y * focal_point[1], 100)

		begin_x = max(focal_point_x - Fraction(result_x, 2), 0)
		begin_y = max(focal_point_y - Fraction(result_y, 2), 0)

		bbox = (
			floor(begin_x),
			floor(begin_y),
			floor(begin_x + result_x),
			floor(begin_y + result_y),
		)

	return CropOp(bbox, resize, (bbox[2] - bbox[0], bbox[3] - bbox[1]))


def scale_and_crop(
	im: Image,
	size: Tuple[int, int],
	crop: Union[bool, str] = False,
	upscale: bool = None,
	zoom: Optional[float] = None,
	target: Optional[Union[Tuple[int, int], str]] = None,
	**kwargs
):
	op = calc_scale_and_crop(im, size, crop=crop, upscale=upscale, zoom=zoom, target=target)
	if op.resize is not None:
		im = im.resize(op.resize, resample=Image.Resampling.LANCZOS)
	return im.crop(op.bbox)
