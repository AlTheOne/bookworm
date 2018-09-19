from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from catalogApp.models import Books, GenreBooks, TagsBooks, Currency
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain


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


class SearchPage(View, MyPagination, InitFilter):
	TEMPLATES = 'catalogApp/catalog-main.html'
	QS = None

	FILTER_GENRES = None
	FILTER_TAGS = None
	FILTER_SORT = None
	CURRENCY = None

	def post(self, *args, **kwargs):
		data = {}
		if self.request.POST.get('q') is not None:
			data['search_q'] = self.request.POST.get('q')

			# Инициализация шаблона
			self.init_view()

			# Инициализация сортировки
			# self.init_filter()

			self.QS = Books.objects.filter(
				Q(title__icontains=data['search_q']) | 
				Q(description__icontains=data['search_q'])
		 		# Q(genre__icontains=data['q'])|
				# Q(tags__icontains=data['q'])
			).reverse()

			data['q-word'] = data['search_q'].split(' ')
			if len(data['q-word']) > 1:
				for q in data['q-word']:
					data['obj'] = Books.objects.filter(
						Q(title__icontains=data['search_q']) | 
						Q(description__icontains=data['search_q'])
						# Q(genre__icontains=data['q'])|
						# Q(tags__icontains=data['q'])
						).reverse()
					self.QS = list(chain(data['search'], data['obj']))

			data['genres'] = GenreBooks.objects.filter(is_active=True).order_by('title')
			data['tags'] = TagsBooks.objects.filter(is_active=True).order_by('title')
			data['currency'] = Currency.objects.filter(is_active=True).order_by('title')

			# Инициализация категорий и меток
			self.init_mainfilter()

			# data['paginator'] = self.mainPaginator(2)

			# Инициализация валют
			self.init_currency()
			data['objects'] = self.QS
			data['get_genres'] = self.FILTER_GENRES
			data['get_tags'] = self.FILTER_TAGS
			data['get_sort'] = self.FILTER_SORT
			data['rune'] = self.CURRENCY
			return render(self.request, self.TEMPLATES, context=data)
		else:
			return redirect('/')