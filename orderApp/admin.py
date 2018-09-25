from django.contrib import admin
from orderApp.models import Order, Status, OrderObjects


class OrderObjectsInline(admin.TabularInline):
	model = OrderObjects
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	class Meta:
		models = Order

	inlines = [OrderObjectsInline,]
	save_on_top = True

	list_display = ('id', 'status', 'name', 'user', 'country', 'city', 'updated', 'created')
	list_display_links = ('name',)
	list_editable = ('status',)
	list_filter = ('is_active', 'status', 'created')
	search_fields = ('status__title', 'name')

admin.site.register(Order, OrderAdmin)


class StatusAdmin(admin.ModelAdmin):
	class Meta:
		models = Status

	list_display = ('id', 'title', 'updated', 'created')
	list_display_links = ('title',)

admin.site.register(Status, StatusAdmin)


class OrderObjectsAdmin(admin.ModelAdmin):
	class Meta:
		models = OrderObjects

	list_display = ('id', 'is_active','content_object', 'price', 'user',)
	list_display_links = ('content_object',)

admin.site.register(OrderObjects, OrderObjectsAdmin)