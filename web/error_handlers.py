# -*- coding: utf-8 -*-
import sys

from django.http import HttpResponseServerError
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils import timezone


def error_500(request, template_name='500.jinja'):
	template = get_template(template_name)
	except_type, value, _ = sys.exc_info()
	return HttpResponseServerError(template.render({
		'date_now': timezone.now().isoformat(),
		'exception_type': except_type.__name__,
		'exception_value': value,
		'request': request
	}))


def error_404(request, exception, template_name='404.jinja'): # pylint: disable=unused-argument
	context = {
		'date_now': timezone.now().isoformat(),
		'request': request,
	}
	return TemplateResponse(request, template_name, context, status=404)
