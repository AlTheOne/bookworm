from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from userApp.models import User


class Status(models.Model):
	class Meta:
		verbose_name=_('Статус заказа')
		verbose_name_plural=_('Статусы заказов')

	title = models.CharField(verbose_name=_('Название'), max_length=30, help_text=_('Не более 30 символов.'))
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title


class OrderObjects(models.Model):
	class Meta:
		verbose_name=_('Товар заказа')
		verbose_name_plural=_('Товар Заказов')

	order = models.ForeignKey('Order', verbose_name=_('Заказ'), related_name='orderobj', on_delete=models.CASCADE, blank=True, null=True)
	# content_type - Какая модель используется
	# object_id - id объекта используемой модели 
	content_type = models.ForeignKey(ContentType, verbose_name=_('Модель'), on_delete=models.CASCADE, help_text=_('Выберите модель'))
	object_id = models.PositiveIntegerField(verbose_name=_('ID объекта'), help_text=_('ID объекта указанной модели'))
	content_object = GenericForeignKey('content_type', 'object_id')
	price = models.DecimalField(verbose_name=_('Цена'), max_digits=10, decimal_places=2, default=0.00, help_text=_('Цена за единицу товара'))
	count = models.PositiveIntegerField(verbose_name=_('Количество'), default=1, help_text=_('Не менее одного'))
	is_active = models.BooleanField(verbose_name=_('Активно'), default=True, help_text=_('Видно пользователям, только если активно'))
	user = models.ForeignKey(User, verbose_name=_('Автор'), on_delete='SET_NULL', blank=True, null=True)


class Order(models.Model):
	class Meta:
		verbose_name=_('Заказ')
		verbose_name_plural=_('Заказы')

	status = models.ForeignKey(Status, verbose_name=_('Статус заказа'), on_delete="SET_NULL", blank=True, null=True)
	name = models.CharField(verbose_name=_('Имя получателя'), max_length=120)
	country = models.CharField(verbose_name=_('Страна/Регион'), max_length=120)
	street = models.CharField(verbose_name=_('Улица, дом, квартира'), max_length=120)
	apt = models.CharField(verbose_name=_('Квартира, блок'), max_length=120, blank=True, null=True, help_text=_('При необходимости'))
	region = models.CharField( verbose_name=_('Край/Область/Регион'), max_length=120,)
	city = models.CharField(verbose_name=_('Город'), max_length=120)
	postcode = models.CharField(verbose_name=_('Почтовый индекс'), max_length=25)
	phone = models.CharField(verbose_name=_('Номер телефона'), max_length=25)
	is_active = models.BooleanField(verbose_name=_('Активно'), default=True, help_text=_('Видно пользователям, только если активно'))
	user = models.ForeignKey(User,verbose_name=_('Автор'), on_delete='SET_NULL', blank=True, null=True)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.name