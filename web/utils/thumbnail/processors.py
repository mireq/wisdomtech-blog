# -*- coding: utf-8 -*-
import re

from PIL import Image
from easy_thumbnails.processors import _compare_entropy


def scale_and_crop(im, size, crop=False, upscale=False, zoom=None, target=None, preserve_aspect=False, **kwargs):
	source_x, source_y = [float(v) for v in im.size]
	target_x, target_y = [int(v) for v in size]

	if crop or not target_x or not target_y:
		scale = max(target_x / source_x, target_y / source_y)
	else:
		scale = min(target_x / source_x, target_y / source_y)

	if not target_x:
		target_x = round(source_x * scale)
	elif not target_y:
		target_y = round(source_y * scale)

	if zoom:
		if not crop:
			target_x = round(source_x * scale)
			target_y = round(source_y * scale)
			crop = True
		scale *= (100 + int(zoom)) / 100.0

	# Resize image if needed
	if scale < 1.0 or (scale > 1.0 and upscale):
		im = im.resize((int(round(source_x * scale)), int(round(source_y * scale))), resample=Image.Resampling.LANCZOS)

	if crop:
		# Use integer values now.
		source_x, source_y = im.size
		# Difference between new image size and requested size.
		diff_x = int(source_x - min(source_x, target_x))
		diff_y = int(source_y - min(source_y, target_y))

		# preserve ratio for smaller images
		if preserve_aspect and (target_x > source_x or target_y > source_y):
			if target_y / source_y > target_x / source_x:
				diff_x = source_x - ((source_y * target_x) // target_y)
			else:
				diff_y = source_y - ((source_x * target_y) // target_x)

		if crop != 'scale' and (diff_x or diff_y):
			if isinstance(target, str):
				target = re.match(r'(\d+)?,(\d+)?$', target)
				if target:
					target = target.groups()
			if target:
				focal_point = [int(n) if (n or n == 0) else 50 for n in target]
			else:
				focal_point = 50, 50
			# Crop around the focal point
			halftarget_x, halftarget_y = int(target_x / 2), int(target_y / 2)
			focal_point_x = int(source_x * focal_point[0] / 100)
			focal_point_y = int(source_y * focal_point[1] / 100)
			box = [
				max(0, min(source_x - target_x, focal_point_x - halftarget_x)),
				max(0, min(source_y - target_y, focal_point_y - halftarget_y)),
			]
			box.append(int(min(source_x, box[0] + target_x)))
			box.append(int(min(source_y, box[1] + target_y)))
			# See if an edge cropping argument was provided.
			edge_crop = (isinstance(crop, str) and re.match(r'(?:(-?)(\d+))?,(?:(-?)(\d+))?$', crop))
			if edge_crop and filter(None, edge_crop.groups()):
				x_right, x_crop, y_bottom, y_crop = edge_crop.groups()
				if x_crop:
					offset = min(int(target_x) * int(x_crop) // 100, diff_x)
					if x_right:
						box[0] = diff_x - offset
						box[2] = source_x - offset
					else:
						box[0] = offset
						box[2] = source_x - (diff_x - offset)
				if y_crop:
					offset = min(int(target_y) * int(y_crop) // 100, diff_y)
					if y_bottom:
						box[1] = diff_y - offset
						box[3] = source_y - offset
					else:
						box[1] = offset
						box[3] = source_y - (diff_y - offset)
			# See if the image should be "smart cropped".
			elif crop == 'smart':
				left = top = 0
				right, bottom = source_x, source_y
				while diff_x:
					image_slice = min(diff_x, max(diff_x // 5, 10))
					start = im.crop((left, 0, left + image_slice, source_y))
					end = im.crop((right - image_slice, 0, right, source_y))
					add, remove = _compare_entropy(start, end, image_slice, diff_x)
					left += add
					right -= remove
					diff_x = diff_x - add - remove
				while diff_y:
					image_slice = min(diff_y, max(diff_y // 5, 10))
					start = im.crop((0, top, source_x, top + image_slice))
					end = im.crop((0, bottom - image_slice, source_x, bottom))
					add, remove = _compare_entropy(start, end, image_slice, diff_y)
					top += add
					bottom -= remove
					diff_y = diff_y - add - remove
				box = (left, top, right, bottom)
			elif preserve_aspect:
				# Move focal point to match diff x / y
				focal_point_x = halftarget_x + min(diff_x, max(-diff_x, 2 * (focal_point_x - halftarget_x))) // 2
				focal_point_y = halftarget_y + min(diff_y, max(-diff_y, 2 * (focal_point_y - halftarget_y))) // 2
				box = [
					max(0, focal_point_x - halftarget_x),
					max(0, focal_point_y - halftarget_y),
				]
				box.append(int(min(source_x, box[0] + source_x - diff_x)))
				box.append(int(min(source_y, box[1] + source_y - diff_y)))

			# Finally, crop the image!
			im = im.crop(box)
	return im
