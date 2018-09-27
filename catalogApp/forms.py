from django import forms
from django.utils.translation import ugettext_lazy as _
from userApp.models import User
from catalogApp.models import *
from tinymce import TinyMCE
from django.db.models import Q



RATE=[('1',''), ('2',''), ('3',''), ('4',''), ('5','')]

class CommentForm(forms.Form):
	message = forms.CharField(label='Текст отзыва', required=True, max_length=512, widget=forms.Textarea)
	rate = forms.ChoiceField(choices=RATE, required=False, widget=forms.RadioSelect(attrs={'class': 'star-rating__input', 'name': 'rate'}))


class AddBookForm(forms.ModelForm):
	class Meta:
		model = Books
		exclude = ('is_active', 'user')

	title = forms.CharField(label='Название', required=True, max_length = 120, help_text=_('Не более 120 символов'), widget=forms.TextInput(attrs={'placeholder': 'Название...'}))
	description = forms.CharField(label='Описание', required=True, widget=TinyMCE())
	author = forms.ModelMultipleChoiceField(queryset=AuthorBooks.objects.all(), required=False, label = _('Автор'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	attributes = forms.ModelMultipleChoiceField(queryset=AttributesBooks.objects.filter(rel_attrib=None), required=False, label = _('Атрибуты'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	genre = forms.ModelMultipleChoiceField(queryset=GenreBooks.objects.all(), required=False, label = _('Жанр'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	phouse = forms.ModelMultipleChoiceField(queryset=PublicHouse.objects.all(), required=False, label = _('Издательство'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	tags = forms.ModelMultipleChoiceField(queryset=TagsBooks.objects.all(), required=False, label = _('Метка'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
	price = forms.DecimalField(max_digits=10, decimal_places=2, label = _('Цена'), help_text = _('Цена за единицу товара'))
	discount = forms.IntegerField(label = _('Скидка'), required=False, help_text=_('В процентах'))
	price_discount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label = _('Цена c учётом скидки'), help_text = _('Заполняется автоматически'), widget=forms.TextInput(attrs={'readonly':True}))
	counter = forms.IntegerField(label = _('Количество'), help_text=_('В наличии'))
	date = forms.IntegerField(label = _('Год издания'))
	preview = forms.ImageField(label = _('Превью'))


class AddAttributeForm(forms.ModelForm):
	class Meta:
		model = AttributesBooks
		fields = '__all__'


class AddAuthorForm(forms.ModelForm):
	class Meta:
		model = AuthorBooks
		exclude = ('user', 'is_active')

class AddTagsForm(forms.ModelForm):
	class Meta:
		model = TagsBooks
		exclude = ('user', 'is_active')
	
	title = forms.CharField(max_length=120, label=_('Название'), widget=forms.TextInput(attrs={'class': 'input_tags_title'}))
	slug = forms.SlugField(max_length=120, label=_('Ссылка'), widget=forms.TextInput(attrs={'class': 'input_tags_slug'}))

class AddGenreForm(forms.ModelForm):
	class Meta:
		model = GenreBooks
		exclude = ('user', 'is_active')
	
	title = forms.CharField(max_length=120, label=_('Название'), widget=forms.TextInput(attrs={'class': 'input_genre_title'}))
	slug = forms.SlugField(max_length=120, label=_('Ссылка'), widget=forms.TextInput(attrs={'class': 'input_genre_slug'}))


class AddPhouseForm(forms.ModelForm):
	class Meta:
		model = PublicHouse
		exclude = ('user', 'is_active')
	
	title = forms.CharField(max_length=120, label=_('Название'), widget=forms.TextInput(attrs={'class': 'input_phouse_title'}))	