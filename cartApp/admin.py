from django.contrib import admin
from cartApp.models import Cart

class CartAdmin(admin.ModelAdmin):
	class Meta:
		models = Cart

	list_display = ('session',)

admin.site.register(Cart, CartAdmin)