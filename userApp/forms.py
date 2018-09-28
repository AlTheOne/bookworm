from django import forms
from userApp.models import User, UserAvatar
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
	login = forms.CharField(label='Логин', required=True, max_length=32, help_text='Логин быть от 4 до 32 символов. В логине могут быть только латинские буквы, цифры и знаки "-" и "_"', widget=forms.TextInput(attrs={'placeholder': 'Ваш логин', 'id':'reg_id_login', 'class':'reg_input_login', 'pattern':'^[a-zA-Z][A-Za-z0-9_\-]{4,32}$'}))
	password = forms.CharField(label='Пароль', required=True, max_length=128, help_text='Пароль должен состатья от 8 до 72 символов содержать буквы разного регистра и хотя бы одну цифру и спец символ', widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль', 'id':'reg_id_password', 'class':'reg_input_password', 'pattern':'^(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'}))
	repassword = forms.CharField(label='Повторите пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Повторить пароль', 'class':'reg_input_repassword'}))
	name = forms.CharField(label='Имя', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class':'reg_input_name', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s]{3,32}$'}))
	surname = forms.CharField(label='Фамилия', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия', 'class':'reg_input_surname', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s]{3,32}$'}))
	email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ваша почта', 'id':'reg_id_email', 'class':'reg_input_email', 'pattern':'^([A-Za-z0-9_\-\.]{4,32})+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'}))
	phone_number = forms.CharField(label='Номер телефона', required=True, max_length=32, validators=[phone_validator], widget=forms.TextInput(attrs={'placeholder': '+7 XXX XXX XX XX', 'class':'reg_input_phone', 'pattern':'^[\+]\d{1,2}\d{3}\d{3}\d{2}\d{2}$'}))

class SettingsForm(forms.Form):
	first_name = forms.CharField(label='Имя', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class':'input_name', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s]{3,32}$'}))
	last_name = forms.CharField(label='Фамилия', required=True, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия', 'class':'input_surname', 'pattern':'^[a-zA-Zа-яА-ЯЁё\s]{3,32}$'}))
	email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ваша почта', 'class':'input_email', 'pattern':'^([A-Za-z0-9_\-\.]{4,32})+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'}))
	phone_number = forms.CharField(label='Номер телефона', required=True, max_length=32, validators=[phone_validator], widget=forms.TextInput(attrs={'placeholder': '+7 XXX XXX XX XX', 'class':'input_phone', 'pattern':'^[\+]\d{1,2}\d{3}\d{3}\d{2}\d{2}$'}))

class ChangeAvatar(forms.ModelForm):
	class Meta:
		model = UserAvatar
		fields = ('avatar', )

class RecoveryEmailForm(forms.Form):
	email = forms.EmailField(label='Почта', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ваша почта'}))

class NewPswdForm(forms.Form):
	password = forms.CharField(label='Пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
	repassword = forms.CharField(label='Повторите пароль', required=True, max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Повторить пароль'}))