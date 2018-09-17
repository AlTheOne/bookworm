from userApp.settings import AuthenticateUsers
from userApp.forms import RegistryForm, RecoveryEmailForm
from userApp.models import UserAvatar
from django.http import HttpResponse

def session(request):
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
	return locals()

def authform(request):
	if not request.user.is_authenticated:
		form_log_in = AuthenticateUsers()
		log_form = form_log_in.init_form()
		form_registry = RegistryForm()
		form_recovery = RecoveryEmailForm()
	else:
		try:
			avatar = UserAvatar.objects.get(user=request.user)
		except:
			avatar = None
	return locals()
