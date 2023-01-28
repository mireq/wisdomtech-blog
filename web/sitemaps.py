# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost


User = get_user_model()


class BlogSitemap(Sitemap):
	changefreq = "never"
	priority = 1

	def items(self):
		return (BlogPost.objects
			.fast_translate(fields=['title', 'slug'])
			.order_by('-pk')
			.values('pk', 'fast_translation_title', 'fast_translation_slug', 'date_updated'))

	def location(self, item):
		return reverse('blog:post_detail', kwargs={'slug': item['fast_translation_slug'], 'pk': item['pk']})

	def lastmod(self, item):
		return item['date_updated']


class UserSitemap(Sitemap):
	changefreq = "never"
	priority = 1

	def items(self):
		return (User.objects
			.filter(is_active=True)
			.order_by('pk')
			.values('pk', 'last_login'))

	def location(self, item):
		return reverse('accounts:user_detail', kwargs={'pk': item['pk']})

	def lastmod(self, item):
		return item['last_login']


sitemaps = {
	'blog': BlogSitemap,
	'user': UserSitemap,
}
