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
		data['myorders'] = Order.objects.filter(user=self.request.user, is_active=True)
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
	def get(self, *args, **kwargs):
		return redirect('mycart')

	def post(self, *args, **kwargs):
		data = {}
		# Если выборка
		if self.request.POST.get('status') == 'buy-selected':
			list_book_id = self.request.POST.getlist('books')
			getbooks = list()
			for i in list_book_id:
				getbooks.append(int(i))
			books = Cart.objects.filter(user=self.request.user, is_active=True, id__in=getbooks)
		# Иначе вся корзина
		else:
			books = Cart.objects.filter(user=self.request.user, is_active=True)
			getbooks = list()
			for i in books:
				getbooks.append(i.id)

		data['getbooks'] = getbooks # список id покупаемых книг для передачи
		data['books'] = books # Список покупаемых книг для отображения
		data['form'] = OrderForm # Форма заказа
		return render(self.request, self.TEMPLATES, context=data)


# Page with form address
class DoOrderBook(View):
	TEMPLATES = 'orderApp/add-order.html'
	def get(self, *args, **kwargs):
		data = {}
		data['id'] = self.kwargs.get('id')
		data['getbooks'] = [data['id'], ]
		data['book'] = get_object_or_404(Cart, id=data['id'], user=self.request.user, is_active=True)
		data['form'] = OrderForm
		return render(self.request, self.TEMPLATES, context=data)


# Create new Order and OrderObjects
# Нужен хотя бы 1 СТАТУС ЗАКАЗА!!!
class DidOrder(View):
	TEMPLATES = 'orderApp/add-order.html'
	def post(self, *args, **kwargs):
		formOrder = OrderForm(self.request.POST)
		if formOrder.is_valid():
			new_order = Order.objects.create(
				name = formOrder.cleaned_data['name'],
				country =formOrder.cleaned_data['country'],
				street = formOrder.cleaned_data['street'],
				apt = formOrder.cleaned_data['apt'],
				region = formOrder.cleaned_data['region'],
				city = formOrder.cleaned_data['city'],
				postcode = formOrder.cleaned_data['postcode'],
				phone = formOrder.cleaned_data['phone'],
				user = self.request.user,
			)
			book = self.request.POST.get('books')
			getbooks = [int(i)for i in book[1:-1].split(', ')]
			books = Cart.objects.filter(user=self.request.user, is_active=True, id__in=getbooks)

			if books:
				for item in books:
					OrderObjects.objects.create(
						order = new_order,
						content_object = item.content_object,
						price = item.content_object.price,
						count = 1,
						is_active = True,
						user = self.request.user
					)

			return redirect('order-info', id=new_order.id)
		# else:
		# 	data['form'] = OrderForm(self.request.POST)

		# 	return render(self.request, self.TEMPLATES, context=data)