from django.shortcuts import render
from django.views.generic import View
from orderApp.models import Order, OrderObjects
from cartApp.models import Cart
from orderApp.forms import OrderForm
from django.shortcuts import get_object_or_404, redirect


# List all orders of user
class MyOrder(View):
	TEMPLATES = 'orderApp/order.html'
	def get(self, *args, **kwargs):
		data = {}
		data['myorders'] = OrderObjects.objects.filter(user=self.request.user, is_active=True)
		return render(self.request, self.TEMPLATES, context=data)


# Page with information about order of user
class OrderInfo(View):
	TEMPLATES = 'orderApp/order-info.html'
	def get(self, *args, **kwargs):
		data = {}
		data['id'] = kwargs.get('id')
		data['myorders'] = get_object_or_404(Order, id=data['id'], user=self.request.user, is_active=True)
		data['objects'] = OrderObjects.objects.filter(order=data['myorders'])
		return render(self.request, self.TEMPLATES, context=data)


# Page with form address
class DoOrder(View):
	TEMPLATES = 'orderApp/add-order.html'
	def post(self, *args, **kwargs):
		data = {}
		data['getbooks'] = self.request.POST.getlist('books')
		data['form'] = OrderForm
		user_name = self.request.user

		data['books'] = Cart.objects.filter(user=user_name, is_active=True, id__in=data['getbooks'])
		return render(self.request, self.TEMPLATES, context=data)

# Page with form address
class DoOrderBook(View):
	TEMPLATES = 'orderApp/add-order.html'
	def get(self, *args, **kwargs):
		data = {}
		data['id'] = self.kwargs.get('id')
		data['getbooks'] = get_object_or_404(Cart, id=data['id'], user=self.request.user, is_active=True)
		data['form'] = OrderForm
		user_name = self.request.user

		return render(self.request, self.TEMPLATES, context=data)

# Create new Order and OrderObjects
# Нужен хотя бы 1 СТАТУС ЗАКАЗА!!!
class DidOrder(View):
	TEMPLATES = 'orderApp/add-order.html'
	def post(self, *args, **kwargs):
		data = {}
		data['form'] = OrderForm(self.request.POST)
		if data['form'].is_valid():
			data['order'] = Order.objects.create(
				status_id = 1, #Здесь статус заказа
				name = data['form'].cleaned_data['name'],
				country = data['form'].cleaned_data['country'],
				street = data['form'].cleaned_data['street'],
				apt = data['form'].cleaned_data['apt'],
				region = data['form'].cleaned_data['region'],
				city = data['form'].cleaned_data['city'],
				postcode = data['form'].cleaned_data['postcode'],
				phone = data['form'].cleaned_data['phone'],
				is_active = True,
				user = self.request.user,
			)

			book = self.request.POST.get('books')
			books = [int(i[1:-1])for i in book[1:-1].split(', ')]

			books_buy = Cart.objects.filter(is_active=True, id__in=books)

			for item in books_buy:
				if item.content_object.discount > 0:
					OrderObjects.objects.create(
						order = data['order'],
						content_object = item.content_object,
						price = item.content_object.price_discount,
						count = 1,
						is_active = True,
						user = self.request.user
					)
				else:
					OrderObjects.objects.create(
						order = data['order'],
						content_object = item.content_object,
						price = item.content_object.price,
						count = 1,
						is_active = True,
						user = self.request.user
					)

			return render(self.request, self.TEMPLATES, context=data)
		else:
			return render(self.request, self.TEMPLATES, context=data)