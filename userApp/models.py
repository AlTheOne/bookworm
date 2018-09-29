from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_delete


class UserAccountManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, login, email, password, **extra_fields):
		if not login:
			raise ValueError('Login must be provided')

		if not email:
			raise ValueError('Email address must be provided')	

		if not password:
			raise ValueError('Password must be provided')

		email = self.normalize_email(email)
		user = self.model(login=login, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, login=None, email=None, password=None, **extra_fields):
		return self._create_user(login, email, password, **extra_fields)

	def create_superuser(self, login, email, password, **extra_fields):
		extra_fields['is_staff'] = True
		extra_fields['is_superuser'] = True

		return self._create_user(login, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	REQUIRED_FIELDS = ['email']
	USERNAME_FIELD = 'login'
 
	objects = UserAccountManager()
 
	login = models.CharField('login', unique=True, blank=False, null=False, max_length=32)
	email = models.EmailField('email', unique=True, blank=False, null=False)
	first_name = models.CharField('first name', blank=True, null=True, max_length=400)
	last_name = models.CharField('last name', blank=True, null=True, max_length=400)
	is_staff = models.BooleanField('staff status', default=False)
	is_active = models.BooleanField('active', default=True)
	phone_number = models.CharField('phone number', unique=True, max_length=20)

	def get_short_name(self):
		return self.email
 
	def get_full_name(self):
		return '%s %s' % (self.first_name, self.last_name)
 
	def __unicode__(self):
		return self.login


class СonfirmationEmailUser(models.Model):
	class Meta:
		verbose_name=_('Подтверждение почты')
		verbose_name_plural=_('Подтверждения почты')

	user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE, help_text=_('Укажите пользователя'))
	code = models.CharField(verbose_name=_('Код подтверждения'), max_length=100, help_text=_('Рандомная строка'))
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)

	def __str__(self):
		return 'Код активации пользователя %s' % self.user.login


class RecoveryPaswdlUser(models.Model):
	class Meta:
		verbose_name=_('Восстановление пароля')
		verbose_name_plural=_('Восстановление паролей')

	user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE, help_text=_('Укажите пользователя'))
	code = models.CharField(verbose_name=_('Код подтверждения'), max_length=100, help_text=_('Рандомная строка'))
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)

	def __str__(self):
		return 'Код восстановления пароля %s' % self.user.login


class UserAvatar(models.Model):
	class Meta:
		verbose_name=_('Аватар')
		verbose_name_plural=_('Аватарки')

	user = models.OneToOneField(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE, help_text=_('Укажите пользователя'), related_name='ava')
	avatar = models.ImageField(upload_to='avatar/', verbose_name=_('Аватарка'), help_text=_('Максимальный размер 100х100'), blank=True, null=True)
	created = models.DateTimeField(verbose_name=_('Создано'), auto_now_add=True, auto_now=False)

	def __str__(self):
		return 'Аватар %s' % self.user.login

@receiver(post_delete, sender=UserAvatar)
def freezer_post_delete_handler(sender, **kwargs):
	freezer = kwargs['instance']
	storage, path = freezer.avatar.storage, freezer.avatar.path
	storage.delete(path)