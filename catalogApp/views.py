from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from catalogApp.models import *
from catalogApp.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json, random
from django.db.models import Avg
from userApp.decorators import only_users



class MyPagination():
	def mainPaginator(self, nmb, *args, **kwargs):
		# self = данные в классе
		# nmb = кол-во записей на странице
		# args = ожидаем QuerySet
		# Пагинация по результатам

		if self.QS.count() <= nmb:
			return None

		data = {}
		data['paginator'] = Paginator(self.QS, nmb)
		page = self.request.GET.get('page')


		try:
			self.QS = data['paginator'].page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			self.QS = data['paginator'].page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			self.QS = data['paginator'].page(data['paginator'].num_pages)

		return data['paginator']


class InitCurrency(object):
	# Инициализация цен
	def init_currency(self, q_type=None, level=None):
		if 'type_currency' in self.request.COOKIES:
			try:
				self.CURRENCY = Currency.objects.get(slug=self.request.COOKIES.get('type_currency'))
			except Currency.DoesNotExist:
				pass
			
			if self.CURRENCY:
				if q_type == 'get':
					if level:
						self.QS.content_object.price = round(self.QS.content_object.price * self.CURRENCY.quota, 2)
						if self.QS.content_object.price_discount:
							self.QS.content_object.price_discount = round(self.QS.content_object.price_discount * self.CURRENCY.quota, 2)
					else:
							self.QS.price = round(self.QS.price * self.CURRENCY.quota, 2)
							if self.QS.price_discount:
								self.QS.price_discount = round(self.QS.price_discount * self.CURRENCY.quota, 2)
				if q_type == 'filter':
					if level:
						for n in range(len(self.QS)):
							self.QS[n].content_object.price = round(self.QS[n].content_object.price * self.CURRENCY.quota, 2)
							if self.QS[n].content_object.price_discount:
								self.QS[n].content_object.price_discount = round(self.QS[n].content_object.price_discount * self.CURRENCY.quota, 2)
					else:
						for n in range(len(self.QS)):
							self.QS[n].price = round(self.QS[n].price * self.CURRENCY.quota, 2)
							if self.QS[n].price_discount:
								self.QS[n].price_discount = round(self.QS[n].price_discount * self.CURRENCY.quota, 2)
		pass


class InitFilter(object):
	# Инициализация шаблона
	def init_view(self):
		if 'type_view' in self.request.COOKIES:
			if self.request.COOKIES.get('type_view') == 'list':
				self.TEMPLATES = 'catalogApp/catalog-main-list.html'
		pass

	# Инициализация сортировки
	def init_filter(self):
		if 'type_filter' in self.request.COOKIES:
			if self.request.COOKIES.get('type_filter') == '2':
				self.FILTER_SORT = 2
				self.QS = self.QS.order_by('created')
			elif self.request.COOKIES.get('type_filter') == '3':
				self.FILTER_SORT = 3
				self.QS = self.QS.order_by('-title')
			elif self.request.COOKIES.get('type_filter') == '4':
				self.FILTER_SORT = 4
				self.QS = self.QS.order_by('title')
			elif self.request.COOKIES.get('type_filter') == '5':
				self.FILTER_SORT = 5
				self.QS = self.QS.order_by('-date')
			elif self.request.COOKIES.get('type_filter') == '6':
				self.FILTER_SORT = 6
				self.QS = self.QS.order_by('date')
			elif self.request.COOKIES.get('type_filter') == '7':
				self.FILTER_SORT = 7
				self.QS = self.QS.order_by('-price')
			elif self.request.COOKIES.get('type_filter') == '8':
				self.FILTER_SORT = 8
				self.QS = self.QS.order_by('price')
			else:
				self.QS = self.QS.order_by('-created')
		pass


	# Инициализация по меткам и жанрам
	def init_mainfilter(self):
		if 'type_genres' in self.request.COOKIES:
			tg = self.request.COOKIES.get('type_genres')
			genres = [int(i) for i in tg[1:-1].split(', ')]
			self.FILTER_GENRES = genres
			self.QS = self.QS.filter(genre__in=genres).distinct()

		if 'type_tags' in self.request.COOKIES:
			tt = self.request.COOKIES.get('type_tags')
			tags = [int(i) for i in tt[1:-1].split(', ')]
			self.FILTER_TAGS = tags
			self.QS = self.QS.filter(tags__in=tags).distinct()
		pass


class CatalogFilter(View):
	def post(self, *args, **kwargs):
		data = {}
		data['type_view'] = self.request.POST.get('type_view')
		data['type_filter'] = self.request.POST.get('type_filter')
		data['type_currency'] = self.request.POST.get('type_currency')
		data['reset'] = self.request.POST.get('reset')

		response = HttpResponse()
		if data['type_view'] is not None:
			if data['type_view'] == 'list':
				response.set_cookie('type_view', 'list')
			else:
				response.delete_cookie('type_view')

		if data['type_filter'] is not None:
			response.set_cookie('type_filter', data['type_filter'])

		if data['type_currency'] is not None:
			response.set_cookie('type_currency', data['type_currency'])

		if data['reset'] is not None:
			response.delete_cookie('type_genres')
			response.delete_cookie('type_tags')
			response.delete_cookie('type_filter')

		return response


class MainCatalog(View, MyPagination, InitFilter, InitCurrency):
	TEMPLATES = 'catalogApp/catalog-main.html'
	QS = None

	FILTER_GENRES = None
	FILTER_TAGS = None
	FILTER_SORT = None
	CURRENCY = None
	
	def get(self, *args, **kwargs):
		data = {}
		# Инициализация шаблона
		self.init_view()

		self.QS = Books.objects.filter(is_active=True)

		# Инициализация сортировки
		self.init_filter()

		data['genres'] = GenreBooks.objects.filter(is_active=True).order_by('title')
		data['tags'] = TagsBooks.objects.filter(is_active=True).order_by('title')
		data['currency'] = Currency.objects.filter(is_active=True).order_by('title')

		# Инициализация категорий и меток
		self.init_mainfilter()

		# Инициализация пагинации
		data['paginator'] = self.mainPaginator(8)

		# Инициализация валют
		self.init_currency(q_type='filter')
		data['objects'] = self.QS
		data['get_genres'] = self.FILTER_GENRES
		data['get_tags'] = self.FILTER_TAGS
		data['get_sort'] = self.FILTER_SORT
		data['rune'] = self.CURRENCY
		return render(self.request, self.TEMPLATES, context=data)

	def post(self, *args, **kwargs):
		data = {}
		self.init_view()
		data['genre'] = self.request.POST.getlist('genre')
		data['tag'] = self.request.POST.getlist('tag')

		response = redirect('catalog-main')
		if data['genre']:
			dg = [int(item) for item in data['genre']]
			response.set_cookie('type_genres', dg)
		else:
			response.delete_cookie('type_genres')

		if data['tag']:
			dt = [int(item) for item in data['tag']]
			response.set_cookie('type_tags', dt)
		else:
			response.delete_cookie('type_tags')

		return response


class BookPage(View, InitCurrency):
	TEMPLATES = 'catalogApp/book-page.html'
	QS = None
	CURRENCY = None

	def get(self, *args, **kwargs):
		data = {}
		if kwargs.get('id'):
			self.QS = get_object_or_404(Books, id=int(kwargs.get('id')), is_active=True)
			data['comments'] = CommentsBook.objects.filter(book=kwargs.get('id'), is_active=True).order_by("-created")
			data['currency'] = Currency.objects.filter(is_active=True).order_by('title')

			# Инициализация валюты
			self.init_currency(q_type='get')

			data['form_comment'] = CommentForm
			# Rating - Integer. It number use how percent in style.
			if data['comments']:
				data['book_rating'] = round((data['comments'].aggregate(Avg('rate')).get('rate__avg') * 100) / 5)
			else:
				data['book_rating'] = False
			
			data['object'] = self.QS
			data['rune'] = self.CURRENCY
			return render(self.request, self.TEMPLATES, context=data)
		else:
			return redirect('/')

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		form = CommentForm(self.request.POST)
		obj = get_object_or_404(Books, id=self.kwargs.get('id'), is_active=True)
		if form.is_valid():
			if form.cleaned_data['rate'] == '':
				rating = 0
			else:
				rating = form.cleaned_data['rate']

			comment = CommentsBook.objects.create(
				book = obj,
				message = form.cleaned_data['message'],
				rate = rating,
				user = self.request.user,
			)
			return redirect('book-page', id=self.kwargs.get('id'))
		else:
			return redirect('book-page', id=self.kwargs.get('id'))


class EditBook(View):
	TEMPLATES = 'catalogApp/catalog-add-book.html'

	@only_users(url='/')
	def get(self, *args, **kwargs):
		data = {}
		obj = Books.objects.get(id=self.kwargs.get('id'), is_active=True)
		data['form_add_book'] = AddBookForm(instance=obj)
		data['form_add_book'].fields["attributes"].queryset = AttributesBooks.objects.filter(Q(rel_attrib=None)|Q(rel_attrib=self.kwargs.get('id')))
		data['form_add_attrib'] = AddAttributeForm
		data['form_add_author'] = AddAuthorForm
		data['form_add_tags'] = AddTagsForm
		data['form_add_genre'] = AddGenreForm
		data['form_add_phouse'] = AddPhouseForm
		return render(self.request, self.TEMPLATES, context=data)

	@only_users(url='/')
	def post(self, *args, **kwargs):
		obj = Books.objects.get(id=self.kwargs.get('id'), is_active=True)
		bookform = AddBookForm(self.request.POST, self.request.FILES, instance=obj)
		if bookform.is_valid():
			bookform.save()
			return redirect('book-page', id=self.kwargs.get('id'))
		else:
			print('НЕ Валидна')
			data = {}
			data['form_add_book'] = bookform
			data['form_add_book'].fields["attributes"].queryset = AttributesBooks.objects.filter(Q(rel_attrib=None)|Q(rel_attrib=self.kwargs.get('id')))
			data['form_add_attrib'] = AddAttributeForm
			data['form_add_author'] = AddAuthorForm
			data['form_add_tags'] = AddTagsForm
			data['form_add_genre'] = AddGenreForm
			data['form_add_phouse'] = AddPhouseForm
			return render(self.request, self.TEMPLATES, context=data)


class AddBook(View):
	TEMPLATES = 'catalogApp/catalog-add-book.html'

	@only_users(url='/')
	def get(self, *args, **kwargs):
		data = {}
		data['form_add_book'] = AddBookForm
		data['form_add_attrib'] = AddAttributeForm
		data['form_add_author'] = AddAuthorForm
		data['form_add_tags'] = AddTagsForm
		data['form_add_genre'] = AddGenreForm
		data['form_add_phouse'] = AddPhouseForm
		return render(self.request, self.TEMPLATES, context=data)

	@only_users(url='/')
	def post(self, *args, **kwargs):
		bookform = AddBookForm(self.request.POST, self.request.FILES)
		if bookform.is_valid():
			bookform.save()
		else:
			data = {}
			data['form_add_book'] = bookform
			data['form_add_attrib'] = AddAttributeForm
			data['form_add_author'] = AddAuthorForm
			data['form_add_tags'] = AddTagsForm
			data['form_add_genre'] = AddGenreForm
			data['form_add_phouse'] = AddPhouseForm
		return render(self.request, self.TEMPLATES, context=data)


class AddAuthorBook(View):
	def get(self, *args, **kwargs):
		return redirect('/')
		
	def post(self, *args, **kwargs):
		data = {}
		authorform = AddAuthorForm(self.request.POST)
		if authorform.is_valid():
			new_object = AuthorBooks.objects.create(
				first_name = authorform.cleaned_data['first_name'],
				secondary_name = authorform.cleaned_data['secondary_name'],
				last_name = authorform.cleaned_data['last_name'],
				user = self.request.user,
			)
			data['status'] = True
			data['id'] = new_object.id
			data['title'] = "%s %s." % (new_object.last_name, new_object.first_name[0])
		else:
			data['status'] = False
		return JsonResponse(data)


class AddAttribBook(View):
	def get(self, *args, **kwargs):
		return redirect('/')
	
	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		attribform = AddAttributeForm(self.request.POST)
		if attribform.is_valid():
			new_object = AttributesBooks.objects.create(
				name = attribform.cleaned_data['name'],
				value = attribform.cleaned_data['value'],
			)
			data['status'] = True
			data['id'] = new_object.id
			data['title'] = new_object.name
		else:
			data['status'] = False
		return JsonResponse(data)


class AddTagBook(View):
	def get(self, *args, **kwargs):
		return redirect('/')

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		tagform = AddTagsForm(self.request.POST)
		if tagform.is_valid():
			new_object = TagsBooks.objects.create(
				title = tagform.cleaned_data['title'],
				slug = tagform.cleaned_data['slug'],
				user = self.request.user,
			)
			data['status'] = True
			data['id'] = new_object.id
			data['title'] = new_object.title
		else:
			data['status'] = False
		return JsonResponse(data)


class AddGenreBook(View):
	def get(self, *args, **kwargs):
		return redirect('/')

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		genreform = AddGenreForm(self.request.POST)
		if genreform.is_valid():
			new_object = GenreBooks.objects.create(
				title = genreform.cleaned_data['title'],
				slug = genreform.cleaned_data['slug'],
				user = self.request.user,
			)
			data['status'] = True
			data['id'] = new_object.id
			data['title'] = new_object.title
		else:
			data['status'] = False
		return JsonResponse(data)


class AddPhouseBook(View):
	def get(self, *args, **kwargs):
		return redirect('/')

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		phouseform = AddPhouseForm(self.request.POST)
		if phouseform.is_valid():
			new_object = PublicHouse.objects.create(
				title = phouseform.cleaned_data['title'],
				user = self.request.user,
			)
			data['status'] = True
			data['id'] = new_object.id
			data['title'] = new_object.title
		else:
			data['status'] = False
		return JsonResponse(data)

