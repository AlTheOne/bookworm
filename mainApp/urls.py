from django.urls import path
from mainApp.views import NewsPage, NewsEditPage

urlpatterns = [
	path('<slug:slug>/', NewsPage.as_view(), name='news-page'),
	path('edit/<slug:slug>/', NewsEditPage.as_view(), name='news-page-edit'),
]