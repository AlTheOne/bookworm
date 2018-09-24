from django.urls import path
from catalogApp.views import MainCatalog, BookPage, AddBook, CatalogFilter, AddAuthorBook, AddAttribBook, AddTagBook, AddGenreBook, AddPhouseBook, EditBook
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', MainCatalog.as_view(), name='catalog-main'),
	path('book/<int:id>/', BookPage.as_view(), name='book-page'),
	path('book-add/', AddBook.as_view(), name='book-add'),
	path('book-edit/<int:id>/', EditBook.as_view(), name='book-edit'),
	path('filter/', CatalogFilter.as_view(), name='book-filter'),
	path('add-author/', AddAuthorBook.as_view(), name='add-author'),
	path('add-attributes/', AddAttribBook.as_view(), name='add-attributes'),
	path('add-tags/', AddTagBook.as_view(), name='add-tags'),
	path('add-genre/', AddGenreBook.as_view(), name='add-genre'),
	path('add-phouse/', AddPhouseBook.as_view(), name='add-phouse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)