# -*- coding: utf-8 -*-
from django_jinja import library
from django.utils.translation import ngettext
from django.utils.formats import number_format


AWERAGE_WPM = 200


def read_time(words: int) -> str:
	minutes = words // AWERAGE_WPM + 1
	text = ngettext(
		"%(min)s minute",
		"%(min)s minutes",
		minutes
	)
	return text % {'min': number_format(minutes)}


library.filter(read_time)
