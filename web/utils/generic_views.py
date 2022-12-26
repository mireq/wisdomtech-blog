# -*- coding: utf-8 -*-
from django.views import generic
from django_universal_paginator.cursor import CursorPaginateMixin


class ListView(CursorPaginateMixin, generic.ListView):
	pass
