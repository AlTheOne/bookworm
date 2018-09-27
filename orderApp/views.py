from django.shortcuts import render
from django.views.generic import View
from orderApp.models import Order, OrderObjects
from catalogApp.models import Books, Currency
from catalogApp.views import InitCurrency
from cartApp.models import Cart
from orderApp.forms import OrderForm
from django.shortcuts import get_object_or_404, redirect
from userApp.decorators import only_users
from django.db.models import F


# List all orders of user
class MyOrder(View):
	TEMPLATES = 'orderApp/order.html'

	@only_users(url='/')
	def get(self, *args, **kwargs):
		data = {}
		print(self.request.session.get('order', False))
		data['myorders'] = Order.objects.filter(user=self.request.user, is_active=True)
		return render(self.request, self.TEMPLATES, context=data)


# Page with information about order of user
class OrderInfo(View):
	TEMPLATES = 'orderApp/order-info.html'
	QS = None
	CURRENCY = None

	@only_users(url='/')
	def get(self, *args, **kwargs):
		data = {}
		data['id'] = kwargs.get('id')
		data['myorders'] = get_object_or_404(Order, id=data['id'], user=self.request.user, is_active=True)
		self.QS = OrderObjects.objects.filter(order=data['myorders'])
		data['currency'] = Currency.objects.filter(is_active=True).order_by('title')

		self.init_currency()
		data['objects'] = self.QS
		data['rune'] = self.CURRENCY
		return render(self.request, self.TEMPLATES, context=data)
	
	# Инициализация цен
	def init_currency(self):
		if 'type_currency' in self.request.COOKIES:
			try:
				self.CURRENCY = Currency.objects.get(slug=self.request.COOKIES.get('type_currency'))
			except Currency.DoesNotExist:
				pass
			
			if self.CURRENCY:
				for n in range(len(self.QS)):
					self.QS[n].price = round(self.QS[n].price * self.CURRENCY.quota, 2)
		pass


# Page with form address
class DoOrder(View, InitCurrency):
	TEMPLATES = 'orderApp/add-order.html'
	QS = None
	CURRENCY = None

	@only_users(url='/')
	def get(self, *args, **kwargs):
		return redirect('mycart')

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		
		# Если выборка
		if self.request.POST.get('status') == 'buy-selected':
			list_book_id = self.request.POST.getlist('books')
			getbooks = list()
			for i in list_book_id:
				getbooks.append(int(i))
			self.QS = Cart.objects.filter(user=self.request.user, is_active=True, id__in=getbooks)
		# Иначе вся корзина
		else:
			self.QS = Cart.objects.filter(user=self.request.user, is_active=True)
			getbooks = list()
			for i in self.QS:
				getbooks.append(i.id)

		self.request.session['order'] = getbooks # список id покупаемых книг для передачи

		# Инициализация валют
		self.init_currency(q_type='filter', level=True)
		data['currency'] = Currency.objects.filter(is_active=True).order_by('title')
		data['rune'] = self.CURRENCY
		data['books'] = self.QS # Список покупаемых книг для отображения
		data['form'] = OrderForm # Форма заказа
		return render(self.request, self.TEMPLATES, context=data)


# Page with form address
class DoOrderBook(View, InitCurrency):
	TEMPLATES = 'orderApp/add-order.html'
	QS = None
	CURRENCY = None

	@only_users(url='/')
	def get(self, *args, **kwargs):
		data = {}
		data['id'] = self.kwargs.get('id')
		self.request.session['order'] = [data['id'], ]
		self.QS = get_object_or_404(Cart, id=data['id'], user=self.request.user, is_active=True)
		data['form'] = OrderForm

		# Инициализация валют
		self.init_currency(q_type='get', level=True)
		data['currency'] = Currency.objects.filter(is_active=True).order_by('title')
		data['rune'] = self.CURRENCY
		data['book'] = self.QS
		return render(self.request, self.TEMPLATES, context=data)


# Create new Order and OrderObjects
class DidOrder(View):
	TEMPLATES = 'orderApp/add-order.html'

	@only_users(url='/')
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
			books = Cart.objects.filter(user=self.request.user, is_active=True, id__in=self.request.session['order'])

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
					Books.objects.filter(id=item.content_object.id).update(counter = (F('counter') - 1))
				books.delete()
			del self.request.session['order']
			return redirect('order-info', id=new_order.id)
		else:
			data = {}
			data['books'] = Cart.objects.filter(user=self.request.user, is_active=True, id__in=self.request.session['order'])
			data['form'] = OrderForm(self.request.POST)
			return render(self.request, self.TEMPLATES, context=data)