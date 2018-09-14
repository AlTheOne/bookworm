from django.urls import path
from orderApp.views import MyOrder, DoOrder, DoOrderBook, DidOrder, OrderInfo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', MyOrder.as_view(), name='order'),
	path('add/', DoOrder.as_view(), name='add-order'),
	path('add/<int:id>/', DoOrderBook.as_view(), name='add-order-1'),
	path('oplata/', DidOrder.as_view(), name='oplata'),
	path('order-info/<int:id>/', OrderInfo.as_view(), name='order-info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)