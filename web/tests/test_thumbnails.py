# -*- coding: utf-8 -*-
from typing import Tuple

from PIL import Image
from django.test import TestCase

from web.utils.thumbnail.processors import calc_scale_and_crop


class ThumbnailTest(TestCase):
	def make_image(self, size: Tuple[int, int]):
		return Image.new('L', size)

	def test_no_action_needed(self):
		size = (10, 10)
		im = self.make_image(size)
		crop = calc_scale_and_crop(im, size)
		self.assertEqual((0, 0, 10, 10), crop.bbox)
		self.assertIsNone(crop.resize)

	def test_scale_down(self):
		im = self.make_image((10, 10))
		crop = calc_scale_and_crop(im, (6, 6))
		self.assertEqual((0, 0, 6, 6), crop.bbox)
		self.assertEqual((6, 6), crop.resize)

		# ceil used to calculate
		im = self.make_image((10, 9))
		crop = calc_scale_and_crop(im, (5, 5))
		self.assertEqual((5, 5), crop.resize)

		# correctly reduce size
		im = self.make_image((8, 10))
		crop = calc_scale_and_crop(im, (5, 5))
		self.assertEqual((4, 5), crop.resize)

	def test_upscale(self):
		im = self.make_image((5, 5))
		crop = calc_scale_and_crop(im, (6, 6))
		self.assertIsNone(crop.resize)

		# properly scale
		crop = calc_scale_and_crop(im, (6, 6), upscale=True)
		self.assertEqual((6, 6), crop.resize)

		# scale to 7
		crop = calc_scale_and_crop(im, (8, 7), upscale=True)
		self.assertEqual((7, 7), crop.resize)

		# scale only to 4
		crop = calc_scale_and_crop(im, (4, 8), upscale=True)
		self.assertEqual((4, 4), crop.resize)

		# test ceil rounding
		im = self.make_image((6, 7))
		crop = calc_scale_and_crop(im, (7, 8), upscale=True)
		self.assertEqual((7, 8), crop.resize)

	def test_crop_resize(self):
		im = self.make_image((7, 6))
		crop = calc_scale_and_crop(im, (5, 5), crop=True)
		self.assertEqual((6, 5), crop.resize)
		self.assertEqual((0, 0, 5, 5), crop.bbox)

		im = self.make_image((100, 200))
		crop = calc_scale_and_crop(im, (100, 100), crop=True)
		self.assertEqual((0, 50, 100, 150), crop.bbox)

		im = self.make_image((75, 110))
		crop = calc_scale_and_crop(im, (100, 100), crop=True)
		self.assertEqual((0, 17, 75, 92), crop.bbox)

		im = self.make_image((75, 110))
		crop = calc_scale_and_crop(im, (100, 100), crop=True, target=(0, 0))
		self.assertEqual((0, 0, 75, 75), crop.bbox)
