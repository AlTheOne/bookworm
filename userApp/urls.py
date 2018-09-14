from django.urls import path
from userApp.views import (UserLogOut, UserLogIn, UserRegistration, 
							UserSettings, UserProfile, UserForgotPswd, UserRecoveryPswd)

urlpatterns = [
	path('profile/', UserProfile.as_view(), name='user-profile'),
	path('profile-settings/', UserSettings.as_view(), name='user-settings'),
	path('logout/', UserLogOut.as_view(), name='user-logout'),
	path('login/', UserLogIn.as_view(), name='user-login'),
	path('registration/', UserRegistration.as_view(), name='registration'),
	path('forgot-password/', UserForgotPswd.as_view(), name='user-forgotpswd'),
	path('recovery-password/<str:code>/', UserRecoveryPswd.as_view(), name='user-recover'),
]