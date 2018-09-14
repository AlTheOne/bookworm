from django.urls import path
from mainApp.views import MainPage

urlpatterns = [
	path('', MainPage.as_view(), name='main-page'),
]