# -*- coding: utf-8 -*-
from .models import User
from blog.models import BlogPost
from web.utils.generic_views import AttachmentListAndUploadView, ListView, DetailView


class UserListView(ListView):
	paginate_by = 10

	def get_queryset(self):
		return (User.objects
			.filter(is_active=True)
			.fast_translate(fields=['subtitle', 'short_description'])
			.select_related('gallery', 'gallery__primary_attachment')
			.only('gallery', 'gallery__primary_attachment', 'username', 'first_name', 'last_name', 'email')
			.order_by('last_name', 'first_name', 'pk')
		)


class UserDetailView(DetailView):
	def get_queryset(self):
		return (User.objects
			.filter(is_active=True)
			.fast_translate()
			.select_related('gallery', 'gallery__primary_attachment')
		)

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		obj = ctx['object']
		last_posts = BlogPost.objects.published().filter(author=obj).fast_translate(fields=['title', 'slug']).only('pk')
		ctx['last_posts'] = last_posts
		return ctx


class UserAttachmentsList(AttachmentListAndUploadView):
	model_class = User
