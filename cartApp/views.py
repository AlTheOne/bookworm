from django.shortcuts import render
from django.views.generic import View
from cartApp.models import Cart
from catalogApp.models import Books, Currency
from catalogApp.views import InitCurrency
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse


class MyCart(View, InitCurrency):
	TEMPLATES = 'cartApp/mycart.html'
	QS = None
	CURRENCY = None

	def get(self, *args, **kwargs):
		data = {}
		session_key = self.request.session.session_key

		if self.request.user.is_authenticated:
			self.QS = Cart.objects.filter(is_active=True, user=self.request.user)
		else:
			self.QS = Cart.objects.filter(is_active=True, session=self.request.session.session_key)


		self.init_currency(q_type='filter', level='True') # Инициализация валют

		data['objects'] = self.QS
		data['currency'] = Currency.objects.filter(is_active=True).order_by('title')
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