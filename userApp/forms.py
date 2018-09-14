from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")


class AuthEmailForm(forms.Form):
	login = forms.EmailField(label='Почта', required=True, max_length=32, help_text='Не более 32 символов', widget=forms.TextInput(attrs={'placeholder': 'Ваша почта'}))
	password = forms.CharField(label='Пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
	remember = forms.CharField(label='Запомнить', required=False, max_length=128, widget=forms.CheckboxInput())

class AuthLoginForm(forms.Form):
	login = forms.CharField(label='Логин', required=True, max_length=32, help_text='Не более 32 символов', widget=forms.TextInput(attrs={'placeholder': 'Ваш логин'}))
	password = forms.CharField(label='Пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
	remember = forms.CharField(label='Запомнить', required=False, max_length=128, widget=forms.CheckboxInput())

class AuthLoginEmailForm(forms.Form):
	login = forms.CharField(label='Логин/Почта', required=True, max_length=32, help_text='Не более 32 символов', widget=forms.TextInput(attrs={'placeholder': 'Ваш логин или почта'}))
	password = forms.CharField(label='Пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
	remember = forms.CharField(label='Запомнить', required=False, max_length=128, widget=forms.CheckboxInput())

class RegistryForm(forms.Form):
	login = forms.CharField(label='Логин', required=True, max_length=32, help_text='Не более 32 символов', widget=forms.TextInput(attrs={'placeholder': 'Ваш логин'}))
	password = forms.CharField(label='Пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
	repassword = forms.CharField(label='Повторите пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Повторить пароль'}))
	name = forms.CharField(label='Имя', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
	surname = forms.CharField(label='Фамилия', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}))
	email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ваша почта'}))
	phone_number = forms.CharField(label='Номер телефона', required=True, max_length=32, validators=[phone_validator], widget=forms.TextInput(attrs={'placeholder': '+7 999 888 77 66'}))

class SettingsForm(forms.Form):
	first_name = forms.CharField(label='Имя', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
	last_name = forms.CharField(label='Фамилия', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}))
	email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ваша почта'}))
	phone_number = forms.CharField(label='Номер телефона', required=True, max_length=32, validators=[phone_validator], widget=forms.TextInput(attrs={'placeholder': '+7 999 888 77 66'}))

class RecoveryEmailForm(forms.Form):
	email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ваша почта'}))

class NewPswdForm(forms.Form):
	password = forms.CharField(label='Пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
	repassword = forms.CharField(label='Повторите пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Повторить пароль'}))