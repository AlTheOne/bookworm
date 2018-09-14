from userApp.models import User

class EmailAuthBackend(object):
	@staticmethod
	def authenticate(self, email=None, password=None):
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return None

		if not user.check_password(password):
			return None

		return user

	@staticmethod
	def get_user(self, user_id):
		try:
			return User.objects.get(id=user_id)
		except User.DoesNotExist:
			return None