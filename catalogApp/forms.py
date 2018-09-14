from django import forms
from django.utils.translation import ugettext_lazy as _
from userApp.models import User
from catalogApp.models import *
from tinymce import TinyMCE


# class CommentForm(forms.Form):
# 	message = forms.CharField(label='Текст отзыва', required=True, max_length=512, widget=forms.TextInput(attrs={'placeholder': 'Ваш отзыв'}))
# 	rate = forms.IntegerField(label='Рейтинг', required=True)

RATE=[('1',''), ('2',''), ('3',''), ('4',''), ('5','')]

class CommentForm(forms.Form):
	message = forms.CharField(label='Текст отзыва', required=True, max_length=512, widget=TinyMCE(mce_attrs={'height':200}))
	rate = forms.ChoiceField(choices=RATE, required=False, widget=forms.RadioSelect(attrs={'class': 'star-rating__input', 'name': 'rate'}))


class FilterForm(forms.Form):
	tags = forms.MultipleChoiceField(choices=TagsBooks.objects.values('title', 'slug'), widget=forms.CheckboxSelectMultiple)

# class AddBookForm(forms.ModelForm):
# 	class Meta:
# 		model = Books
# 		fields = '__all__'


# class AddBookForm(forms.Form):
# 	title = forms.CharField(label='Название', required=True, max_length = 120, help_text=_('Не более 120 символов'), widget=forms.TextInput(attrs={'placeholder': 'Название...'}))
# 	slug = forms.SlugField(label='Ссылка', max_length=128, help_text = _('Не более 128 символов'), widget=forms.TextInput(attrs={'placeholder': 'Ссылка...'}))
# 	description = forms.CharField(label=_('Описание'), widget=forms.Textarea())
# 	author = forms.MultipleChoiceField(AuthorBooks, label = _('Автор'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
# 	# attributes = forms.MultipleChoiceField(choices=AttributesBooks.objects.all(), widget=forms.CheckboxSelectMultiple)
# 	# genre = forms.MultipleChoiceField(choices=GenreBooks.objects.all(), label = _('Жанр'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
# 	# tags = forms.MultipleChoiceField(choices=TagsBooks.objects.all(), label = _('Метка'), help_text = _('Зажмите shift, чтобы выбрать несколько вариантов'))
# 	price = forms.DecimalField(max_digits=10, decimal_places=2, label = _('Цена'), help_text = _('Цена за единицу товара'))
# 	discount = forms.IntegerField(label = _('Скидка'), help_text=_('В процентах'))
# 	price_discount = forms.DecimalField(max_digits=10, decimal_places=2, label = _('Цена c учётом скидки'), help_text = _('Заполняется автоматически'))
# 	counter = forms.IntegerField(label = _('Количество'), help_text=_('В наличии'))
# 	preview = forms.ImageField(label = _('Превью'))
# 	user = forms.ChoiceField(choices=User, label = _('Опубликовал'))
# 	is_active = forms.BooleanField(label = _('Активировать'))