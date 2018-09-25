from django.urls import path
from cartApp.views import MyCart, AddCartFunc, DelCartFunc

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', MyCart.as_view(), name='mycart'),
	path('add/', AddCartFunc.as_view(), name='addcartfunc'),
	path('del/', DelCartFunc.as_view(), name='delcartfunc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)