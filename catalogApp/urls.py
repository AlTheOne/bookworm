from django.urls import path
from catalogApp.views import MainCatalog, TagsCatalog, BookPage, GenerCatalog, AddBook, CatalogFilter,FullAdd
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', MainCatalog.as_view(), name='catalog-main'),
	path('book/<int:id>/', BookPage.as_view(), name='book-page'),
	path('bookadd/', AddBook.as_view(), name='book-add'),
	path('filter/', CatalogFilter.as_view(), name='book-filter'),
	path('add/', FullAdd.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)