from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from userApp.models import User


class Cart(models.Model):
	class Meta:
		verbose_name=_('Корзина')
		verbose_name_plural=_('Корзины')

	session = models.CharField(max_length=256, verbose_name=_('ID сессии'))
	# content_type - Какая модель используется
	# object_id - id объекта используемой модели 
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('Модель'), help_text=_('Выберите модель'))
	object_id = models.PositiveIntegerField(verbose_name=_('ID объекта'), help_text=_('ID объекта указанной модели'))
	content_object = GenericForeignKey('content_type', 'object_id')
	count = models.PositiveIntegerField(default=1, verbose_name=_('Количество'), help_text=_('Не менее одного'))
	is_active = models.BooleanField(default=True, verbose_name=_('Активно'), help_text=_('Видно пользователям, только если активно'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name=_('Автор'))
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Создано'))

	def __str__(self):
		return self.session