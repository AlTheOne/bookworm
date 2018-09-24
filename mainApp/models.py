from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import HTMLField


class News(models.Model):
	class Meta:
		verbose_name = _('Статичная страница')
		verbose_name_plural = _('Статичные страницы')
	
	title = models.CharField(verbose_name = _('Название'), max_length = 120, unique=True, help_text=_('Не более 120 символов'))
	slug = models.SlugField(verbose_name = _('URL'), max_length = 120, unique=True, help_text=_('Не более 120 символов'))
	text = HTMLField('Текст',)
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return self.title