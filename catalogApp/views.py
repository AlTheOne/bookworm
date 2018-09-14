from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from catalogApp.models import *
# from catalogApp.models import Books, GenreBooks, TagsBooks, CommentsBook
from catalogApp.forms import CommentForm, FilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json, random
from django.db.models import Avg


class MyPagination():
	def mainPaginator(self, nmb, *args, **kwargs):
		# self = данные в классе
		# nmb = кол-во записей на странице
		# args = ожидаем QuerySet
		# Пагинация по результатам
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
				self.QS = self.QS.order_by('-created')
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
				self.QS = self.QS.order_by('created')
		pass

	# Инициализация цен
	def init_currency(self):
		if 'type_currency' in self.request.COOKIES:
			try:
				self.CURRENCY = Currency.objects.get(slug=self.request.COOKIES.get('type_currency'))
	
				for n in range(len(self.QS)):
					self.QS[n].price =  round(self.QS[n].price * self.CURRENCY.quota, 2)
					self.QS[n].price_discount = round(self.QS[n].price_discount * self.CURRENCY.quota, 2)

			except Currency.DoesNotExist:
				pass
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

		return response


class MainCatalog(View, MyPagination, InitFilter):
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
		self.init_currency()
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


class TagsCatalog(View):
	TEMPLATES = 'catalogApp/catalog-main.html'
	def get(self, *args, **kwargs):
		data = {}
		data['objects'] = Books.objects.filter(tags__slug=kwargs.get('tag_name'), is_active=True)
		data['genres'] = GenreBooks.objects.filter(is_active=True).order_by('title')
		data['tags'] = TagsBooks.objects.filter(is_active=True).order_by('title')
		return render(self.request, self.TEMPLATES, context=data)


class GenerCatalog(View):
	TEMPLATES = 'catalogApp/catalog-main.html'
	def get(self, *args, **kwargs):
		data = {}
		data['objects'] = Books.objects.filter(gener__slug=kwargs.get('gener_name'), is_active=True)
		data['genres'] = GenreBooks.objects.filter(is_active=True).order_by('title')
		data['tags'] = TagsBooks.objects.filter(is_active=True).order_by('title')
		return render(self.request, self.TEMPLATES, context=data)


class AddBook(View):
	TEMPLATES = 'catalogApp/catalog-add-book.html'
	def get(self, *args, **kwargs):
		data = {}
		# data['form_add_book'] = AddBookForm
		return render(self.request, self.TEMPLATES, context=data)

	def post(self, *args, **kwargs):
		pass


class BookPage(View):
	TEMPLATES = 'catalogApp/book-page.html'
	def get(self, *args, **kwargs):
		data = {}
		if kwargs.get('id'):
			data['object'] = Books.objects.get(id=int(kwargs.get('id')), is_active=True)
			data['comments'] = CommentsBook.objects.filter(book=kwargs.get('id'), is_active=True).order_by("-created")
			data['form_comment'] = CommentForm
			data['book_rating'] = data['comments'].aggregate(Avg('rate'))
			return render(self.request, self.TEMPLATES, context=data)
		else:
			return redirect('/')

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


		# try:
		# 	obj = Books.objects.get(id=self.kwargs.get('id'), is_active=True)
		# except Books.DoisNotExist:
		# 	data['form_comment'] = form
		# 	return render(self.request, self.TEMPLATES, context=data)
		# else:
		# 	if form.is_valid():
		# 		comment = CommentsBook.objects.create(
		# 			book = obj,
		# 			message = form.cleaned_data['message'],
		# 			rate = form.cleaned_data['rate'],
		# 			user = self.request.user,
		# 		)
		# 		comment.save()
		# 		return redirect('book-page', id=self.kwargs.get('id'))
		# 	else:
		# 		data['form_comment'] = form
		# 		return render(self.request, self.TEMPLATES, context=data)


class FullAdd(View):
	def get(self, *args, **kwargs):
		title_list = ('CSS', 'JS', 'C++', 'C#', 'HTML', 'HTML5', 'Java', 'Ruby On Rails', 'SQL', 'Go', 'Golang', 'Python', 'Delphi', 'MySQL', 'PostgreSQL', 'MariaDB', 'Oracle')

		author_fn = ('А.', 'В.', 'Н.', 'Х.', 'Л.', 'Д.', '.М.', 'Т.', 'И.')
		author_ln = ('Ооба', 'Джонсон', 'Морис', 'Андресон', 'Алдерсон', 'Смит', 'Карнеги', 'Блэк')

		attr_name = ('Кол-во страниц', 'Переводчик', 'Возрастное ограничение', 'Переплёт', 'Формат')

		def addNewObj():
			# author = AuthorBooks.objects.create(
			# 	first_name = random.choice(author_fn),
			# 	last_name = random.choice(author_ln)
			# )
			# author.save()

			# attributes = AttributesBooks.objects.create(
			# 	name = random.choice(attr_name),
			# 	value = random.uniform(100, 2000)
			# )

			book = Books.objects.create(
				title = random.choice(title_list) + random.choice(title_list) + random.choice(title_list),
				description = random.choice(title_list)*50,
				# author = author,
				# attributes = attributes,
				# genre = random.randint(5, 12),
				# tags = random.randint(5, 9),
				price = random.uniform(100, 2000),
				discount = random.randint(0, 10),
				counter = random.randint(100, 500),
				preview = 'catalogApp/preview/%d.jpg' % random.randint(1, 50),
				user = self.request.user,
				is_active = True
			)
			# book.author.set(author)
			# book.attributes.set(attributes)
			# book.genre.set(GenreBooks.objects.get(id=random.randint(5, 12)))
			# book.tags.set(TagsBooks.objects.get(id=random.randint(5, 9)))
			# book.save()

		i = 0
		while i<10:
			i = i+1
			addNewObj()
		return redirect('catalog-main')