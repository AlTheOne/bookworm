from django.shortcuts import render
from django.views.generic import View
from cartApp.models import Cart
from catalogApp.models import Books
from catalogApp.models import Currency
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse


class InitFilter(object):
	# Инициализация цен
	def init_currency(self):
		if 'type_currency' in self.request.COOKIES:
			try:
				self.CURRENCY = Currency.objects.get(slug=self.request.COOKIES.get('type_currency'))
	
				for n in range(len(self.QS)):
					self.QS[n].content_object.price = round(self.QS[n].content_object.price * self.CURRENCY.quota, 2)
					self.QS[n].content_object.price_discount = round(self.QS[n].content_object.price_discount * self.CURRENCY.quota, 2)

			except Currency.DoesNotExist:
				pass
		pass


class MyCart(View, InitFilter):
	TEMPLATES = 'cartApp/mycart.html'
	QS = None
	CURRENCY = None

	def get(self, *args, **kwargs):
		data = {}
		session_key = self.request.session.session_key

		if self.request.user.is_authenticated:
			self.QS = Cart.objects.filter(is_active=True, user=self.request.user)

		self.init_currency() # Инициализация валют

		data['objects'] = self.QS
		data['rune'] = self.CURRENCY
		return render(self.request, self.TEMPLATES, context=data)


class AddCartFunc(View):
	def post(self, *args, **kwargs):
		incart = self.request.POST.get('incart')
		myobject = get_object_or_404(Books, id=incart, is_active=True)
		session_key = self.request.session.session_key

		if self.request.user.id is not None:
			Cart.objects.create(
				session = self.request.session.session_key,
				content_object = myobject,
				is_active=True,
				user=self.request.user,
			)
		else:
			Cart.objects.create(
				session = self.request.session.session_key,
				content_object = myobject,
				is_active=True,
			)

		data = {}
		data['status'] = 200
		return JsonResponse(data)


class DelCartFunc(View):
	def post(self, *args, **kwargs):
		outcart = self.request.POST.get('outcart')
		session_key = self.request.session.session_key
		myobject = get_object_or_404(Cart, id=outcart, is_active=True)

		myobject.delete()

		data = {}
		data['status'] = 200
		return JsonResponse(data)