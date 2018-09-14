from django.shortcuts import render
from django.views.generic import View
from catalogApp.models import Books
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
		data['paginator'] = Paginator(*args, nmb)
		page = self.request.GET.get('page')

		try:
			data['resultPage'] = data['paginator'].page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			data['resultPage'] = data['paginator'].page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			data['resultPage'] = data['paginator'].page(data['paginator'].num_pages)

		return (data['resultPage'], data['paginator'])


class SearchPage(View, MyPagination):
	TEMPLATE = 'catalogApp/catalog-main.html'
	def post(self, *args, **kwargs):
		data = {}
		if self.request.POST.get('q') is not None:
			data['q'] = self.request.POST.get('q')
			
			data['search'] = Books.objects.filter(
				Q(title__icontains=data['q']) | 
				Q(description__icontains=data['q'])
				# Q(genre__icontains=data['q'])|
				# Q(tags__icontains=data['q'])
			).reverse()

			data['q-word'] = data['q'].split(' ')
			if len(data['q-word']) > 1:
				for q in data['q-word']:
					data['obj'] = Books.objects.filter(
						Q(title__icontains=data['q']) | 
						Q(description__icontains=data['q'])
						# Q(genre__icontains=data['q'])|
						# Q(tags__icontains=data['q'])
						).reverse()
					data['search'] = list(chain(data['search'], data['obj']))

			data['objects'], data['paginator'] = self.mainPaginator(20, data['search'])
			data['search_q'] = self.request.POST.get('q')
			return render(self.request, self.TEMPLATE, context=data)
		else:
			return render(self.request, self.TEMPLATE, context=data)