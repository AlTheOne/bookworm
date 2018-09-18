from functools import wraps
from django.shortcuts import redirect

def only_users(function=None, url=None):
	def decorator(function):
		@wraps(function)
		def wrapper(self, request, *args, **kwargs):
			if not request.user.is_authenticated:
				return redirect(url)
			else:
				return function(self, request, *args, **kwargs)
		return wrapper
	return decorator


def only_guests(function=None, url=None):
	def decorator(function):
		@wraps(function)
		def wrapper(self, request, *args, **kwargs):
			if request.user.is_authenticated:
				return redirect(url)
			else:
				return function(self, request, *args, **kwargs)
		return wrapper
	return decorator