from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from userApp.models import User


class Cart(models.Model):
	class Meta:
		verbose_name=_('Корзина')
		verbose_name_plural=_('Корзины')

	session = models.CharField(verbose_name=_('ID сессии'), max_length=256)
	# content_type - Какая модель используется
	# object_id - id объекта используемой модели 
	content_type = models.ForeignKey(ContentType, verbose_name=_('Модель'), on_delete=models.CASCADE,  help_text=_('Выберите модель'))
	object_id = models.PositiveIntegerField(verbose_name=_('ID объекта'), help_text=_('ID объекта указанной модели'))
	content_object = GenericForeignKey('content_type', 'object_id')
	count = models.PositiveIntegerField(verbose_name=_('Количество'), default=1, help_text=_('Не менее одного'))
	is_active = models.BooleanField(verbose_name=_('Активно'), default=True, help_text=_('Видно пользователям, только если активно'))
	user = models.ForeignKey(User, verbose_name=_('Автор'), on_delete=models.SET_NULL, blank=True, null=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.session