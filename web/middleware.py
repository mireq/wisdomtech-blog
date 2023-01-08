# -*- coding: utf-8 -*-
class ContentSecurityPolicyMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		response.headers['Content-Security-Policy'] = 'frame-ancestors \'self\' example.com'
		return response
