# -*- coding: utf-8 -*-
import json
from typing import Optional, List

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.http.response import HttpResponseServerError, HttpResponseBadRequest, JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from django_attachments.fields import LibraryField, GalleryField
from django_attachments.models import Library, Attachment
from django_universal_paginator.cursor import CursorPaginateMixin


class ListView(CursorPaginateMixin, generic.ListView):
	pass


class RedirectOnBadSlugMixin(object):
	def redirect_on_bad_slug(self):
		# if request contains slug
		if 'slug' in self.kwargs:
			obj = self.get_object()
			# compare requested slug to object slug
			requested_slug = self.kwargs['slug']
			obj_slug = obj.fast_translation_slug if hasattr(obj, 'fast_translation_slug') else obj.slug
			if requested_slug != obj_slug:
				return HttpResponsePermanentRedirect(obj.get_absolute_url())


class DetailView(RedirectOnBadSlugMixin, generic.DetailView):
	def get_object(self, *args, **kwargs):
		"""
		Get cached object
		"""
		obj = getattr(self, 'object', None)
		if obj is None:
			obj = super().get_object(*args, **kwargs)
			self.object = obj
		return obj

	def dispatch(self, request, *args, **kwargs):
		"""
		Check object slug and redirect if needed
		"""
		if self.request.method == 'GET':
			return self.redirect_on_bad_slug() or super().dispatch(request, *args, **kwargs)

		return super().dispatch(request, *args, **kwargs)


class AttachmentListAndUploadView(PermissionRequiredMixin, generic.ListView):
	"""
	View used to list and uplaod libraries
	"""

	model_class = None
	library_fields = None
	template_name = 'generic/attachments.html'
	permission_required = 'django_attachments.change_attachment'

	def get_library_fields(self) -> Optional[List[str]]:
		return self.library_fields

	def get_model_class(self) -> models.Model:
		return self.model_class

	def get_model_instance(self, fields=None) -> models.Model:
		qs = self.get_model_class()._default_manager.filter(pk=self.kwargs['pk'])
		if fields is not None:
			qs = qs.only(*fields)
		return get_object_or_404(qs)

	def get_library_ids(self) -> List[int]:
		fields = self.get_library_fields()
		# Search all library fields if model has not defined any
		if fields is None:
			fields = [
				field.name
				for field in self.get_model_class()._meta.get_fields()
				if isinstance(field, LibraryField)
			]

		# get attached objecct
		instance = self.get_model_instance(fields)

		# returns all relevant ID's
		return [
			getattr(instance, f'{field}_id')
			for field in fields
			if getattr(instance, f'{field}_id') is not None
		]

	def get_queryset(self):
		return (Attachment.objects
			.filter(library__in=self.get_library_ids())
			.order_by('-pk'))

	def error_response(self, msg):
		return HttpResponseServerError(json.dumps({'error': msg}), content_type="application/json")

	def bad_request_response(self, msg):
		return HttpResponseBadRequest(json.dumps({'error': msg}), content_type="application/json")

	def post(self, request, *args, **kwargs):
		if not 'file' in request.FILES:
			return self.bad_request_response("POST data has no file attribute")

		# find gallery field
		field = None
		for f in self.get_model_class()._meta.get_fields():
			if isinstance(f, GalleryField):
				field = f

		if field is None:
			return self.error_response("Model has no gallery field")

		instance = self.get_model_instance()

		# get or create library
		library = getattr(instance, field.name, None)
		if library is None:
			library = Library()
			library.save()
			setattr(instance, field.name, library)
			instance.save(update_fields=[field.name])

		# save attachment
		attachment = Attachment.objects.create(file=request.FILES['file'], library=library)

		return JsonResponse({'location': attachment.file.url})
