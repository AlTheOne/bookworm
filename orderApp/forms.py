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

	name = forms.CharField(label='Ваше имя', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class':'input_name', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s]{3,120}$'}))
	country = forms.CharField(label='Страна/Регион', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Страна/Регион', 'class':'input_country', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s.,]{3,120}$'}))
	street = forms.CharField(label='Улица, дом, квартира', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира', 'class':'input_street', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s.,0-9]{3,120}$'}))
	apt = forms.CharField(label='Квартира, блок', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Квартира, блок', 'class':'input_apt', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s.,0-9]{3,120}$'}))
	region = forms.CharField(label='Край/Область/Регион', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Край/Область/Регион', 'class':'input_region', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s.,]{3,120}$'}))
	city = forms.CharField(label='Город', required=True, max_length=120, help_text='Не более 120 символов', widget=forms.TextInput(attrs={'placeholder': 'Город', 'class':'input_city', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s0-9.,]{3,120}$'}))
	postcode = forms.CharField(label='Почтовый индекс', required=True, widget=forms.TextInput(attrs={'placeholder': 'Почтовый индекс', 'class':'input_code', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s0-9.,]{3,120}$'}))
	phone = forms.CharField(label='Номер телефона', required=True, max_length=32, validators=[phone_validator], widget=forms.TextInput(attrs={'placeholder': '+7 999 888 77 66', 'class':'input_phone', 'pattern':'^[\+]\d{1,2}\d{3}\d{3}\d{2}\d{2}$'}))