from django.urls import path
from searchApp.views import SearchPage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', SearchPage.as_view(), name='search-main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)