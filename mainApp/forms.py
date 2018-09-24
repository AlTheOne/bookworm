from django import forms
from django.utils.translation import ugettext_lazy as _
from mainApp.models import News
from tinymce import TinyMCE


class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = '__all__'