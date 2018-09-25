from django import template

register = template.Library()

@register.filter
def decpoint(value):
	return str(value).replace(",",".")