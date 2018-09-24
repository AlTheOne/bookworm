from django.urls import path
from mainApp.views import NewsPage

urlpatterns = [
	path('<slug:slug>/', NewsPage.as_view(), name='news-page'),
]