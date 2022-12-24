# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel

from web.utils.models import TimestampModelMixin


User = get_user_model()


class BlogPost(TimestampModelMixin, TranslatableModel, models.Model):
	author = models.ForeignKey(
		User,
		verbose_name=_("Author"),
		on_delete=models.PROTECT
	)

