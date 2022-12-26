# -*- coding: utf-8 -*-
from .models import BlogPost
from web.utils.generic_views import ListView


class BlogPostListView(ListView):
	paginate_by = 1

	def get_queryset(self):
		return (BlogPost.objects
			.published()
			.fast_translate(fields=['title', 'slug', 'summary'])
			.select_related('gallery', 'gallery__primary_attachment')
		)
