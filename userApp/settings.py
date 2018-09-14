from userApp.forms import AuthEmailForm, AuthLoginForm, AuthLoginEmailForm
from userApp.backends.main_auth import EmailAuthBackend
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class AuthenticateUsers(object):
	# METHOD_LOG_IN = 'USERNAME'
	# METHOD_LOG_IN = 'EMAIL'
	METHOD_LOG_IN = 'EMAIL_AND_USERNAME'

	def init_form(self):
		if self.METHOD_LOG_IN == 'EMAIL_AND_USERNAME':
			return AuthLoginEmailForm
		elif self.METHOD_LOG_IN == 'EMAIL':
			return AuthEmailForm
		else:
			return AuthLoginForm

	def interface_data(self):
		if self.METHOD_LOG_IN == 'EMAIL_AND_USERNAME':
			return self.emailLoginAuth()
		elif self.METHOD_LOG_IN == 'EMAIL':
			return self.emailAuth()
		else:
			return self.loginAuth()

	def emailAuth(self):
		get_form = self.init_form()
		form = get_form(self.request.POST)
		return_msg = None
		if form.is_valid():
			email = form.cleaned_data['login']
			password = form.cleaned_data['password']
			user_obj = EmailAuthBackend.authenticate(self.request, email=email, password=password)
			if user_obj is not None:
				if self.request.POST.get('remember') != 'on':
					self.request.session.set_expiry(0)
				login(self.request, user_obj, backend='django.contrib.auth.backends.ModelBackend') 
			else:
				return_msg = 'Неверные данные'
		else:
			return_msg = 'Некорректные данные'
		return return_msg


	def loginAuth(self):
		get_form = self.init_form()
		form = get_form(self.request.POST)
		return_msg = None
		if form.is_valid():
			username = form.cleaned_data['login']
			password = form.cleaned_data['password']
			user_obj = authenticate(self.request, username=username, password=password)
			if user_obj is not None:
				if self.request.POST.get('remember') != 'on':
					self.request.session.set_expiry(0)
				login(self.request, user_obj)
			else:
				return_msg = 'Неверные данные'
		else:
			return_msg = 'Некорректные данные'
		return return_msg

	def emailLoginAuth(self):
		try:
			validate_email(self.request.POST.get('login'))
			return self.emailAuth()
		except ValidationError:
			return self.loginAuth()





# 	def loginAuth(self):
# 		if self.FORMM.is_valid():
# 			login = self.FORMM.cleaned_data['login']
# 			password = self.FORMM.cleaned_data['password']
# 			self.USER = authenticate(self.request, username=login, password=password)
# 			self.MESSAGE = 'Неправильный логин или пароль'
# 			pass
# 		else:
# 			self.MESSAGE = 'Некорректные данные'
# 			pass
# 	def loginEmailAuth(self):
# 		try:
# 			validate_email(self.request.POST.get('login'))
# 			self.emailAuth()
# 		except ValidationError:
# 			self.loginAuth()
# 		pass