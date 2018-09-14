from bookworm.celery import app
from django.core.mail import send_mail


@app.task
def otherMail(**kwargs):
	subject = kwargs.get('subject', None)
	message = kwargs.get('message', '')
	from_email = 'saske1277@yandex.ru'
	html_message = kwargs.get('html_message', None)
	recipient_list = []
	recipient_list.append(kwargs.get('email', None))
	if subject or html_message or html_message or kwargs.get('email', None) is not None:
		send_mail(
			subject=subject, 
			message=message, 
			from_email=from_email, 
			html_message=html_message, 
			recipient_list=recipient_list
		)
	pass


@app.task
def verifyEmail(**kwargs):
	toemail = kwargs.get('email', None)
	uname = kwargs.get('username', None)
	code = kwargs.get('code', None)
	if toemail or uname or code is not None:
		subject = 'Shop: Проверка почты'
		message = ''
		from_email = 'saske1277@yandex.ru'
		html_message="""
			Здравствуйте уважаемый %s!
			<p>Подтвердите ваш адрес электронной почты пройдя по <a href="http://127.0.0.1:8000/user/email-confirm/%s/">этой ссылке</a></p>
		""" % (uname, code)
		recipient_list = []
		recipient_list.append(toemail)
		send_mail(
			subject=subject, 
			message=message, 
			from_email=from_email, 
			html_message=html_message, 
			recipient_list=recipient_list
		)
	pass


@app.task
def recoveryAccount(xtoemail, xcode):
	toemail = xtoemail
	code = xcode
	if toemail or code is not None:
		subject = 'Восстановление пароля'
		message = ''
		from_email = 'saske1277@yandex.ru'
		html_message="""
			Чтобы восстановить пароль - перейдите по <a href="http://127.0.0.1:8000/user/new-passwrd/%s/">этой ссылке</a>
		""" % code
		recipient_list = list()
		recipient_list.append(toemail)
		send_mail(
			subject=subject, 
			message=message, 
			from_email=from_email, 
			html_message=html_message, 
			recipient_list=recipient_list
		)
	pass


@app.task
def okRecoveryAccount(**kwargs):
	toemail = kwargs.get('email', None)
	uname = kwargs.get('username', None)
	if toemail or uname is not None:
		subject = 'Ваш пароль успешно изменён'
		message = ''
		from_email = 'saske1277@yandex.ru'
		html_message="""
			Ваш пароль успешно изменён!<br>
			Поздравляем %s!!!
		""" % uname
		recipient_list = []
		recipient_list.append(toemail)
		send_mail(
			subject=subject, 
			message=message, 
			from_email=from_email, 
			html_message=html_message, 
			recipient_list=recipient_list
		)
	pass


@app.task
def helloMail():
	subject = 'Здарова МУЖИК'
	message = ''
	from_email = 'saske1277@yandex.ru'
	html_message = '''
		Я решил поздароваться с тобой!!!<br>
		<h1 style="color:blue;"><strong>ЗДРАВСТВУЙ</strong></h1>

	'''
	recipient_list = []
	recipient_list.append('saske1277@gmail.com')
	send_mail(
		subject=subject, 
		message=message, 
		from_email=from_email, 
		html_message=html_message, 
		recipient_list=recipient_list
	)
	pass