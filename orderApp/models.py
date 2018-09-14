from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from userApp.models import User


class Status(models.Model):
	class Meta:
		verbose_name=_('Статус заказа')
		verbose_name_plural=_('Статусы заказов')

	title = models.CharField(max_length = 30, help_text=_('Не более 30 символов.'), verbose_name=_('Название'))
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Обновлено'))
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Создано'))

	def __str__(self):
		return self.title


class OrderObjects(models.Model):
	class Meta:
		verbose_name=_('Товар заказа')
		verbose_name_plural=_('Товар Заказов')

	order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name=_('Заказ'), blank=True, null=True)
	# content_type - Какая модель используется
	# object_id - id объекта используемой модели 
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Модель'), help_text=_('Выберите модель'))
	object_id = models.PositiveIntegerField(verbose_name=_('ID объекта'), help_text=_('ID объекта указанной модели'))
	content_object = GenericForeignKey('content_type', 'object_id')
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name = _('Цена'), help_text = _('Цена за единицу товара'))
	count = models.PositiveIntegerField(default=1, verbose_name=_('Количество'), help_text=_('Не менее одного'))
	is_active = models.BooleanField(default=True, verbose_name=_('Активно'), help_text=_('Видно пользователям, только если активно'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name=_('Автор'))


class Order(models.Model):
	class Meta:
		verbose_name=_('Заказ')
		verbose_name_plural=_('Заказы')

	status = models.ForeignKey(Status, on_delete="SET_NULL", verbose_name=_('Статус заказа'))
	name = models.CharField(max_length=120, verbose_name=_('Имя получателя'), null=True)
	country = models.CharField(max_length=120, verbose_name=_('Страна/Регион'), null=True)
	street = models.CharField(max_length=120, verbose_name=_('Улица, дом, квартира'), null=True)
	apt = models.CharField(max_length=120, blank=True, null=True, verbose_name=_('Квартира, блок'), help_text=_('При необходимости'))
	region = models.CharField(max_length=120, verbose_name=_('Край/Область/Регион'), null=True)
	city = models.CharField(max_length=120, verbose_name=_('Город'), null=True)
	postcode = models.PositiveIntegerField(verbose_name=_('Почтовый индекс'), null=True)
	phone = models.CharField(max_length=25, verbose_name=_('Номер телефона'), null=True)
	is_active = models.BooleanField(default=True, verbose_name=_('Активно'), help_text=_('Видно пользователям, только если активно'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name=_('Автор'))
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Обновлено'))
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Создано'))

	def __str__(self):
		return self.name