from django.contrib import admin
from orderApp.models import Order, Status, OrderObjects


class OrderObjectsInline(admin.TabularInline):
	model = OrderObjects
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	class Meta:
		models = Order

	inlines = [OrderObjectsInline,]

admin.site.register(Order, OrderAdmin)


class StatusAdmin(admin.ModelAdmin):
	class Meta:
		models = Status

admin.site.register(Status, StatusAdmin)


class OrderObjectsAdmin(admin.ModelAdmin):
	class Meta:
		models = OrderObjects

admin.site.register(OrderObjects, OrderObjectsAdmin)