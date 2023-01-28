# -*- coding: utf-8 -*-
from .models import User
from web.utils.generic_views import AttachmentListAndUploadView, ListView, DetailView


class UserListView(ListView):
	paginate_by = 10

	def get_queryset(self):
		return (User.objects
			.filter(is_active=True)
			.fast_translate(fields=['subtitle', 'short_description'])
			.select_related('gallery', 'gallery__primary_attachment')
			.only('gallery', 'gallery__primary_attachment', 'username', 'first_name', 'last_name', 'email')
			.order_by('pk')
		)


class UserDetailView(DetailView):
	def get_queryset(self):
		return (User.objects
			.filter(is_active=True)
			.fast_translate()
			.select_related('gallery', 'gallery__primary_attachment')
		)


class UserAttachmentsList(AttachmentListAndUploadView):
	model_class = User
