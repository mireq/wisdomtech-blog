# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.template.defaulttags import date
from django.utils import timezone
from django.utils.formats import number_format
from django.utils.translation import ngettext
from django_jinja import library


AWERAGE_WPM = 200


def read_time(words: int) -> str:
	minutes = words // AWERAGE_WPM + 1
	text = ngettext(
		"%(min)s minute",
		"%(min)s minutes",
		minutes
	)
	return text % {'min': number_format(minutes)}


def now(format_string):
	tzinfo = timezone.get_current_timezone() if settings.USE_TZ else None
	return date(datetime.now(tz=tzinfo), format_string)


library.filter(read_time)
library.global_function(now)
