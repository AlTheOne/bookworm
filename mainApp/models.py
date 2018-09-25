from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import HTMLField


class News(models.Model):
	class Meta:
		verbose_name=_('Статичная страница')
		verbose_name_plural=_('Статичные страницы')
	
	title = models.CharField(verbose_name=_('Название'), max_length=120, unique=True, help_text=_('Не более 120 символов'))
	slug = models.SlugField(verbose_name=_('URL'), max_length=120, unique=True, help_text=_('Не более 120 символов'))
	text = HTMLField('Текст',)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title