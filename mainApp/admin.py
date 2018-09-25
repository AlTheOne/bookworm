from django.contrib import admin
from mainApp.models import News


class NewsAdmin(admin.ModelAdmin):
	class Meta:
		model = News
	
	list_display = ('id', 'title', 'is_active', 'updated', 'created')
	list_editable = ('is_active',)
	list_display_links = ('title',)

admin.site.register(News, NewsAdmin)