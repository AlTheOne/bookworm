from django.contrib import admin
from userApp.models import User, UserAvatar, СonfirmationEmailUser, RecoveryPaswdlUser

class UserAdmin(admin.ModelAdmin):
	class Meta:
		model = User

	save_on_top = True

	list_display = ('id', 'login', 'email', 'is_active', 'is_staff', 'is_superuser')
	list_display_links = ('login',)
	list_filter = ('is_active', 'is_staff', 'is_superuser')
	search_fields = ('login', 'email')

admin.site.register(User, UserAdmin)


class UserAvatarAdmin(admin.ModelAdmin):
	class Meta:
		model = UserAvatar

	list_display = ('id', 'user')
	list_display_links = ('user',)
	search_fields = ('user__login',)

admin.site.register(UserAvatar, UserAvatarAdmin)

admin.site.register(СonfirmationEmailUser)
admin.site.register(RecoveryPaswdlUser)