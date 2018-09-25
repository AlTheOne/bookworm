from django.contrib import admin
from cartApp.models import Cart

class CartAdmin(admin.ModelAdmin):
	class Meta:
		models = Cart

	fields = (('session', 'is_active'), ('content_type', 'object_id'), 'count', 'user')
	list_display = ('id', 'is_active', 'session', 'user', 'created')
	list_display_links = ('id', 'session',)
	list_editable = ('is_active',)
	list_filter = ('is_active', 'created')
	readonly_fields = ('session',)
	search_fields = ('user__login',)
	show_full_result_count = False

admin.site.register(Cart, CartAdmin)