from django.contrib import admin
from userApp.models import User, UserAvatar

class UserAdmin(admin.ModelAdmin):
	class Meta:
		model = User

	list_display = ('id', 'login', 'is_active', 'is_staff', 'is_superuser')
	list_display_links = ('id', 'login')

admin.site.register(User, UserAdmin)


class UserAvatarAdmin(admin.ModelAdmin):
	class Meta:
		model = UserAvatar

	list_display = ('id', 'user')
	list_display_links = ('id', 'user')

admin.site.register(UserAvatar, UserAvatarAdmin)