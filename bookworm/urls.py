from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('user/', include('userApp.urls')),
    path('search/', include('searchApp.urls')),
    path('mycart/', include('cartApp.urls')),
    path('order/', include('orderApp.urls')),
    # path('mainapp/', include('mainApp.urls')),
    path('', include('catalogApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)