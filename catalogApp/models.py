from django.db import models
from userApp.models import User
from django.utils.translation import ugettext_lazy as _
from tinymce import HTMLField
from decimal import Decimal


class GenreBooks(models.Model):
	class Meta:
		verbose_name = _('Жанр')
		verbose_name_plural = _('Жанры')

	title = models.CharField(max_length = 120, verbose_name = _('Название жанра'), unique=True, help_text=_('Не более 120 символов'))
	slug = models.SlugField(max_length=128, unique=True, null=True, blank=True, verbose_name = _('Ссылка'), help_text = _('Не более 128 символов'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name = _('Продавец'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return self.title

class AuthorBooks(models.Model):
	class Meta:
		verbose_name = _('Автор')
		verbose_name_plural = _('Авторы')

	first_name = models.CharField(max_length = 120, verbose_name = _('Имя'), help_text=_('Не более 120 символов'))
	secondary_name = models.CharField(max_length = 120, blank=True, null=True, verbose_name = _('Отчество'), help_text=_('Не более 120 символов'))
	last_name = models.CharField(max_length = 120, verbose_name = _('Фамилия'), help_text=_('Не более 120 символов'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name = _('Продавец'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return '%s %s.' % (self.last_name, self.first_name[0])


class TagsBooks(models.Model):
	class Meta:
		verbose_name = _('Метка')
		verbose_name_plural = _('Метки')

	title = models.CharField(max_length = 120, verbose_name = _('Название метки'), unique=True, help_text=_('Не более 120 символов'))
	slug = models.SlugField(max_length=128, unique=True, null=True, blank=True, verbose_name = _('Ссылка'), help_text = _('Не более 128 символов'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name = _('Продавец'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return self.title


class PublicHouse(models.Model):
	class Meta:
		verbose_name = _('Издательство')
		verbose_name_plural = _('Издательства')

	title = models.CharField(max_length = 120, verbose_name = _('Название издательства'), unique=True, help_text=_('Не более 120 символов'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name = _('Продавец'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return self.title


class AttributesBooks(models.Model):
	class Meta:
		verbose_name = _('Атрибут книги')
		verbose_name_plural = _('Атрибуты книг')

	name = models.CharField(max_length = 120, verbose_name = _('Название аттрибута'), help_text=_('Не более 120 символов'))
	value = models.CharField(max_length=128, null=True, blank=True, verbose_name = _('Значение'), help_text = _('Не более 128 символов'))

	def __str__(self):
		return '%d. %s' % (self.id, self.name)


class Books(models.Model):
	class Meta:
		verbose_name = _('Книга')
		verbose_name_plural = _('Книги')

	title = models.CharField(max_length = 120, verbose_name = _('Название'), help_text=_('Не более 120 символов'))
	description = HTMLField('Описание',)
	author = models.ManyToManyField(AuthorBooks, blank=True, verbose_name = _('Автор'), related_name='rel_author', help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	date = models.CharField(max_length = 4, verbose_name = _('Дата выхода'), blank=True, help_text=_('Не более 4 символов'))
	attributes = models.ManyToManyField(AttributesBooks, blank=True, verbose_name = _('Аттрибуты'), related_name='rel_attrib', help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	phouse = models.ManyToManyField(PublicHouse, blank=True, verbose_name = _('Издательство'), related_name='rel_phouse', help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	genre = models.ManyToManyField(GenreBooks, blank=True, verbose_name = _('Жанр'), related_name='rel_genre', help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	tags = models.ManyToManyField(TagsBooks, blank=True, verbose_name = _('Метка'), related_name='rel_tag', help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name = _('Цена'), help_text = _('Цена за единицу товара'))
	discount = models.IntegerField(default=0, null=True, blank=True, verbose_name = _('Скидка'), help_text=_('В процентах'))
	price_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name = _('Цена c учётом скидки'), help_text = _('Заполняется автоматически'))
	counter = models.IntegerField(default=0, null=True, blank=True, verbose_name = _('Количество'), help_text=_('В наличии'))
	preview = models.ImageField(upload_to='catalogApp/preview/', verbose_name = _('Превью'))
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name = _('Опубликовал'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.discount != 0 and self.discount is not None:
			obj_price = self.price
			self.price_discount = Decimal(obj_price) - (Decimal(obj_price) * (Decimal(self.discount) / 100))
		super(Books, self).save(*args, **kwargs)


class CommentsBook(models.Model):
	class Meta:
		verbose_name = _('Отзыв')
		verbose_name_plural = _('Отзывы')

	book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name=_('Книга'))
	message = HTMLField('Отзыв',)
	rate = models.IntegerField(default=0, verbose_name=_('Рейтинг'), help_text=_('От 1 до 10'), null=True, blank=True)
	user = models.ForeignKey(User, on_delete='SET_NULL', blank=True, null=True, verbose_name = _('Опубликовал'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))


class Currency(models.Model):
	class Meta:
		verbose_name = _('Валюта')
		verbose_name_plural = _('Валюты')

	title = models.CharField(max_length = 120, verbose_name = _('Название'), help_text=_('Не более 120 символов'))
	slug = models.SlugField(max_length = 120, verbose_name = _('Транслит'), help_text=_('Не более 120 символов'))
	rune = models.CharField(max_length = 12, blank=True, verbose_name = _('Символ'), help_text=_('Не более 12 символов'))
	quota = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name = _('Курс'), help_text = _('Цена относительно доллара'))
	is_active = models.BooleanField(default = True, verbose_name = _('Активировать'))
	created = models.DateTimeField(auto_now_add=True ,auto_now=False, verbose_name=_('Создано'))
	updated = models.DateTimeField(auto_now_add=False ,auto_now=True, verbose_name=_('Обновлено'))

	def __str__(self):
		return self.title