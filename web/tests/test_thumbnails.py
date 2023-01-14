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

		# this should reduce height
		im = self.make_image((10, 9))
		crop = calc_scale_and_crop(im, (5, 5))
		self.assertEqual((5, 4), crop.resize)

		# in this case is not possible to use x axis as primary, reduce y
		im = self.make_image((8, 10))
		crop = calc_scale_and_crop(im, (5, 5))
		self.assertEqual((4, 5), crop.resize)

		# one coordinate bigger, one lower
		im = self.make_image((6, 4))
		crop = calc_scale_and_crop(im, (5, 5))
		self.assertEqual((5, 3), crop.resize)

	def test_upscale(self):
		im = self.make_image((5, 5))
		crop = calc_scale_and_crop(im, (6, 6))
		self.assertIsNone(crop.resize)

		crop = calc_scale_and_crop(im, (6, 6), upscale=True)
		self.assertEqual((6, 6), crop.resize)
