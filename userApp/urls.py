from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from userApp.views import (UserLogOut, UserLogIn, UserRegistration, 
							UserSettings, UserProfile, UserForgotPswd, UserRecoveryPswd, UsersAvatar, UserActivating)

urlpatterns = [
	path('profile/', UserProfile.as_view(), name='user-profile'),
	path('profile-settings/', UserSettings.as_view(), name='user-settings'),
	path('avatar-settings/', UsersAvatar.as_view(), name='avatar-settings'),
	path('logout/', UserLogOut.as_view(), name='user-logout'),
	path('login/', UserLogIn.as_view(), name='user-login'),
	path('registration/', UserRegistration.as_view(), name='registration'),
	path('forgot-password/', UserForgotPswd.as_view(), name='user-forgotpswd'),
	path('recovery-password/<str:code>/', UserRecoveryPswd.as_view(), name='user-recover'),
	path('email-confirm/<str:code>/', UserActivating.as_view(), name='email-confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)