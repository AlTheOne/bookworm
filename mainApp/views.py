from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from mainApp.models import News


class NewsPage(View):
    TEMPLATES = 'mainApp/static-page.html'
    def get(self, *args, **kwargs):
        data = {}
        data['news'] = get_object_or_404(News, slug=self.kwargs.get('slug'), is_active=True)
        return render(self.request, self.TEMPLATES, context=data)
    
    def post(self, *args, **kwargs):
        return redirect('/')