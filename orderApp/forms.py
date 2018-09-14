from django import forms
from django.utils.translation import ugettext_lazy as _
from userApp.models import User
from orderApp.models import Order
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ('status', 'is_active', 'user', 'updated', 'created')

	name = forms.CharField(label='Ваше имя', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
	country = forms.CharField(label='Страна/Регион', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Страна/Регион'}))
	street = forms.CharField(label='Улица, дом, квартира', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}))
	apt = forms.CharField(label='Квартира, блок', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Квартира, блок'}))
	region = forms.CharField(label='Край/Область/Регион', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Край/Область/Регион'}))
	city = forms.CharField(label='Город', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Город'}))
	postcode = forms.IntegerField(label='Почтовый индекс', required=True)
	phone = forms.CharField(label='Номер телефона', required=True, max_length=32, validators=[phone_validator], widget=forms.TextInput(attrs={'placeholder': '+7 999 888 77 66'}))