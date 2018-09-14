from django.shortcuts import render
from django.views.generic import View

class MainPage(View):
    TEMPLATES = 'mainApp/index.html'
    def get(self, *args, **kwargs):
        data = {}
        return render(self.request, self.TEMPLATES, context=data)