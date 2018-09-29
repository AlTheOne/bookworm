from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from userApp.settings import AuthenticateUsers
from userApp.forms import RegistryForm, SettingsForm, RecoveryEmailForm, NewPswdForm, ChangeAvatar
from userApp.models import User, UserAvatar, RecoveryPaswdlUser, СonfirmationEmailUser
from userApp.decorators import only_users, only_guests
from django.contrib.auth import logout
from userApp import tasks
from random import choice
from string import ascii_letters
from django.utils import timezone


class UserLogOut(View):
	# Action for Logout
	def get(self, *args, **kwargs):
		logout(self.request)
		return redirect('/')


class UserLogIn(View, AuthenticateUsers):
	# Get data form of Auth

	@only_guests(url='/')
	def post(self, *args, **kwargs):
		data = {}

		error = self.interface_data()
		if error is not None:
			data['sys_err_message'] = error
			data['log_form'] = self.init_form()
		
		return redirect('/')


class UserProfile(View):
	TEMPLATES = 'userApp/user-profile.html'

	@only_users(url='/')
	def get(self, *args, **kwargs):
		data = {}
		user_data = User.objects.get(id=self.request.user.id)
		data['settingsform'] = SettingsForm(initial={
			'first_name': user_data.first_name, 
			'last_name': user_data.last_name,
			'email': user_data.email,
			'phone_number': user_data.phone_number,
		})
		try:
			data['avatar'] = UserAvatar.objects.get(user=self.request.user)
		except UserAvatar.DoesNotExist:
			data['avatar'] = None
		
		data['avatarform'] = ChangeAvatar
		return render(self.request, self.TEMPLATES, context=data)


class UserRegistration(View):
	TEMPLATES = 'userApp/registry.html'
	ERR_MESSAGE = None
	FORMM = None

	# Страница с формой регистрации
	@only_guests(url='/')
	def get(self, *args, **kwargs):
		data = {}
		data['registryform'] = RegistryForm
		return render(self.request, self.TEMPLATES, context=data)

	# Приём данных формы регистрации
	@only_guests(url='/')
	def post(self, *args, **kwargs):
		data = {}
		self.FORMM = RegistryForm(self.request.POST)
		if self.request.POST.get('password') == self.request.POST.get('repassword'):
			if self.FORMM.is_valid():
				try:
					user_data = User.objects.create_user(
						login = self.FORMM.cleaned_data['login'],
						email = self.FORMM.cleaned_data['email'],
						password = self.FORMM.cleaned_data['password'],
						first_name = self.FORMM.cleaned_data['name'],
						last_name = self.FORMM.cleaned_data['surname'],
						phone_number = self.FORMM.cleaned_data['phone_number'],
						is_active = False
					)
				except:
					data['alert'] = 'Ошибка заполнения'
					data['registryform'] = self.FORMM
					return render(self.request, self.TEMPLATES, context=data)

				code = ''.join(choice(ascii_letters) for i in range(50))
				code_data = СonfirmationEmailUser.objects.create(user=user_data, code=code)
				code_data.save()
				tasks.verifyEmail.delay(code=code_data.code, username=user_data.login, email=user_data.email)
				return redirect('/')
			else:
				data['registryform'] = self.FORMM
				return render(self.request, self.TEMPLATES, context=data)
		else:
			data['alert'] = 'Пароли не совпадают'
			data['registryform'] = self.FORMM
			return render(self.request, self.TEMPLATES, context=data)


# Изменение данных пользователя
class UserSettings(View):
	TEMPLATES = 'userApp/settings.html'
	FORMM = None

	@only_users(url='/')
	def get(self, *args, **kwargs):
		return redirect('/')

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		self.FORMM = SettingsForm(self.request.POST)
		if self.FORMM.is_valid():
			obj0 = User.objects.filter(id=self.request.user.id)
			obj0.update(
				first_name = self.FORMM.cleaned_data['first_name'],
				last_name = self.FORMM.cleaned_data['last_name'],
				email = self.FORMM.cleaned_data['email'],
				phone_number = self.FORMM.cleaned_data['phone_number']
			)
			return redirect('user-profile')
		else:
			data['alert'] = 'Ошибка'
			user_data = User.objects.get(id=self.request.user.id)
			data['settingsform'] = SettingsForm(initial={
				'first_name': user_data.first_name, 
				'last_name': user_data.last_name,
				'email': user_data.email,
				'phone_number': user_data.phone_number,
			})
			return render(self.request, self.TEMPLATES, context=data)


class UsersAvatar(View):
	FORMM = None

	@only_users(url='/')
	def post(self, *args, **kwargs):
		data = {}
		self.FORMM = ChangeAvatar(self.request.POST, self.request.FILES)
		if self.FORMM.is_valid():
			data['avatar'] = UserAvatar.objects.filter(user_id=self.request.user.id).delete()
			form_commit = self.FORMM.save(commit=False)
			form_commit.user = self.request.user
			form_commit.save()
			return redirect('user-profile')
		else:
			return redirect('/')


# Страница с новым паролем
class UserRecoveryPswd(View):
	TEMPLATES = 'userApp/new-pswd.html'

	@only_guests(url='/')
	def get(self, *args, **kwargs):
		data = {}
		code = kwargs.get('code', None)
		if code is not None:
			try:
				obj = RecoveryPaswdlUser.objects.get(code=code)
			except:
				return redirect('/')
			if (timezone.now() - obj.created).days >= 1:
				data['alert'] = 'Срок действия ссылки истёк, вы можете запросить новоё письмо в профиле'
				obj.delete()
				return render(self.request, self.TEMPLATES, context=data)
			else:
				data['form_recovery_pswd'] = NewPswdForm
				return render(self.request, self.TEMPLATES, context=data)
		else:
			return redirect('/')

 
class UserForgotPswd(View):
	TEMPLATES = 'userApp/forgot-pswd.html'

	@only_guests(url='/')
	def get(self, *args, **kwargs):
		data = {}
		data['form_recovery_pswd'] = RecoveryEmailForm
		return render(self.request, self.TEMPLATES, context=data)

	@only_guests(url='/')	
	def post(self, *args, **kwargs):
		data = {}
		form = RecoveryEmailForm(self.request.POST)
		if form.is_valid():
			try:
				user_data = User.objects.get(email=form.cleaned_data['email'])
			except:
				data['alert'] = 'Пользователя с такой почтой не найдено'
				data['form_recovery_pswd'] = RecoveryEmailForm
				return render(self.request, self.TEMPLATES, context=data)
			data['alert'] = 'Сообщение с инструкциями восстановления отправлены на почту'
			code = ''.join(choice(ascii_letters) for i in range(50))
			code_data = RecoveryPaswdlUser.objects.create(user=user_data, code=code)
			code_data.save()
			tasks.recoveryAccount.delay(xcode=code, xtoemail=user_data.email)
			return render(self.request, self.TEMPLATES, context=data)
		else:
			data['alert'] = 'Не корректные данные'
			data['form_recovery_pswd'] = RecoveryEmailForm
		return render(self.request, self.TEMPLATES, context=data)


class UserActivating(View):
	@only_guests(url='/')
	def get(self, *args, **kwargs):
		data = {}
		code = kwargs.get('code', None)
		if code is not None:
			obj = get_object_or_404(ConfirmationEmailUser, code=code)
			if (timezone.now() - obj.created).days >= 1:
				data['alert'] = 'Срок действия ссылки истёк, отправляем новое'
				code = ''.join(choice(ascii_letters) for i in range(50))
				code_data = СonfirmationEmailUser.objects.create(user=obj.user, code=code)
				obj.delete()
				code_data.save()
				tasks.verifyEmail.delay(code=code_data.code, username=code_data.user.login, email=code_data.user.email)
		return redirect('/')