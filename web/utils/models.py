# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimestampModelMixin(models.Model):
	date_created = models.DateTimeField(
		_("Date created"),
		editable=False
	)
	date_updated = models.DateTimeField(
		_("Date updated"),
		editable=False
	)

	def save(self, *args, **kwargs):
		self.date_updated = timezone.now()
		if not self.id and not self.date_created:
			self.date_created = self.date_updated
		return super().save(*args, **kwargs)

	class Meta:
		abstract = True
