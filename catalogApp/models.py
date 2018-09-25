from django.db import models
from userApp.models import User
from django.utils.translation import ugettext_lazy as _
from tinymce import HTMLField
from decimal import Decimal
from django.template.defaultfilters import truncatechars
from django.dispatch import receiver
from django.db.models.signals import post_delete


class GenreBooks(models.Model):
	class Meta:
		verbose_name=_('Жанр')
		verbose_name_plural=_('Жанры')

	title = models.CharField(verbose_name=_('Название жанра'), unique=True,  max_length=120, help_text=_('Не более 120 символов'))
	slug = models.SlugField(verbose_name =_('Ссылка'), unique=True, max_length=128, help_text=_('Не более 128 символов'))
	user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete='SET_NULL', blank=True, null=True)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title


class AuthorBooks(models.Model):
	class Meta:
		verbose_name=_('Автор')
		verbose_name_plural=_('Авторы')

	first_name = models.CharField(verbose_name=_('Имя'), max_length=120, help_text=_('Не более 120 символов'))
	secondary_name = models.CharField(verbose_name=_('Отчество'), max_length=120, blank=True, null=True, help_text=_('Не более 120 символов'))
	last_name = models.CharField(verbose_name=_('Фамилия'), max_length=120, help_text=_('Не более 120 символов'))
	user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete='SET_NULL', blank=True, null=True,)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return '%s %s.' % (self.last_name, self.first_name[0])


class TagsBooks(models.Model):
	class Meta:
		verbose_name=_('Метка')
		verbose_name_plural=_('Метки')

	title = models.CharField(verbose_name=_('Название метки'), max_length=120, unique=True, help_text=_('Не более 120 символов'))
	slug = models.SlugField(verbose_name=_('Ссылка'), max_length=128, unique=True, help_text=_('Не более 128 символов'))
	user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete='SET_NULL', blank=True, null=True)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title


class PublicHouse(models.Model):
	class Meta:
		verbose_name=_('Издательство')
		verbose_name_plural=_('Издательства')

	title = models.CharField(verbose_name=_('Название издательства'), max_length=120, unique=True, help_text=_('Не более 120 символов'))
	user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete='SET_NULL', blank=True, null=True)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title


class AttributesBooks(models.Model):
	class Meta:
		verbose_name=_('Атрибут книги')
		verbose_name_plural=_('Атрибуты книг')

	name = models.CharField(max_length=120, verbose_name=_('Название аттрибута'), help_text=_('Не более 120 символов'))
	value = models.CharField(verbose_name=_('Значение'), max_length=128, null=True, blank=True, help_text=_('Не более 128 символов'))

	def __str__(self):
		return '%d. %s' % (self.id, self.name)


class Books(models.Model):
	class Meta:
		verbose_name=_('Книга')
		verbose_name_plural=_('Книги')

	title = models.CharField(verbose_name=_('Название'), max_length=120, help_text=_('Не более 120 символов'))
	description = HTMLField('Описание',)
	author = models.ManyToManyField(AuthorBooks, verbose_name=_('Автор'), related_name='rel_author', blank=True, help_text=_('Зажмите shift, чтобы выбрать несколько вариантов'))
	date = models.CharField(verbose_name=_('Дата выхода'), max_length=4, blank=True, help_text=_('Не более 4 символов'))
	attributes = models.ManyToManyField(AttributesBooks, verbose_name=_('Аттрибуты'), related_name='rel_attrib', blank=True, help_text=_('Зажмите shift, чтобы выбрать несколько вариантов'))
	phouse = models.ManyToManyField(PublicHouse, verbose_name=_('Издательство'), related_name='rel_phouse', help_text=_('Зажмите shift, чтобы выбрать несколько вариантов'))
	genre = models.ManyToManyField(GenreBooks, verbose_name=_('Жанр'), related_name='rel_genre', help_text=_('Зажмите shift, чтобы выбрать несколько вариантов'))
	tags = models.ManyToManyField(TagsBooks, verbose_name=_('Метка'), related_name='rel_tag', blank=True, help_text=_('Зажмите shift, чтобы выбрать несколько вариантов'))
	price = models.DecimalField(verbose_name=_('Цена'), max_digits=10, decimal_places=2, default=0.00, help_text=_('Цена за единицу товара'))
	discount = models.IntegerField(verbose_name=_('Скидка'), default=0, null=True, blank=True, help_text=_('В процентах'))
	price_discount = models.DecimalField(verbose_name=_('Цена c учётом скидки'), max_digits=10, decimal_places=2, default=0.00, blank=True, null=True, help_text=_('Заполняется автоматически'))
	counter = models.IntegerField(verbose_name=_('Количество'), default=0, null=True, blank=True, help_text=_('В наличии'))
	preview = models.ImageField(upload_to='catalogApp/preview/', verbose_name=_('Превью'))
	user = models.ForeignKey(User, verbose_name=_('Опубликовал'), on_delete='SET_NULL', blank=True, null=True)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.discount != 0 and self.discount is not None:
			obj_price = self.price
			self.price_discount = Decimal(obj_price) - (Decimal(obj_price) * (Decimal(self.discount) / 100))
		super(Books, self).save(*args, **kwargs)


@receiver(post_delete, sender=Books)
def freezer_post_delete_handler(sender, **kwargs):
	freezer = kwargs['instance']
	storage, path = freezer.preview.storage, freezer.preview.path
	storage.delete(path)


class CommentsBook(models.Model):
	class Meta:
		verbose_name=_('Отзыв')
		verbose_name_plural=_('Отзывы')

	book = models.ForeignKey(Books, verbose_name=_('Книга'), on_delete=models.CASCADE)
	message = HTMLField('Отзыв',)
	rate = models.IntegerField(verbose_name=_('Рейтинг'), default=0, help_text=_('От 1 до 5'), null=True, blank=True)
	user = models.ForeignKey(User, verbose_name=_('Опубликовал'), on_delete=models.CASCADE, blank=True, null=True)
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	@property
	def short_message(self):
		return truncatechars(self.message, 100)

class Currency(models.Model):
	class Meta:
		verbose_name=_('Валюта')
		verbose_name_plural=_('Валюты')

	title = models.CharField(verbose_name=_('Название'), max_length=120, help_text=_('Не более 120 символов'))
	slug = models.SlugField(verbose_name=_('Транслит'), unique=True, max_length=120, help_text=_('Не более 120 символов'))
	rune = models.CharField(verbose_name=_('Символ'), unique=True, max_length=12, help_text=_('Не более 12 символов'))
	quota = models.DecimalField(verbose_name=_('Курс'), max_digits=10, decimal_places=2, default=0.00, help_text=_('Цена относительно доллара'))
	is_active = models.BooleanField(verbose_name=_('Активировать'), default=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name=_('Обновлено'), auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title