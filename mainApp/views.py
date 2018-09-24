from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from mainApp.models import News
from mainApp.forms import NewsForm


class NewsPage(View):
    TEMPLATES = 'mainApp/static-page.html'
    def get(self, *args, **kwargs):
        data = {}
        data['news'] = get_object_or_404(News, slug=self.kwargs.get('slug'), is_active=True)
        return render(self.request, self.TEMPLATES, context=data)
    
    def post(self, *args, **kwargs):
        return redirect('/')


class NewsEditPage(View):
    TEMPLATES = 'mainApp/static-page-edit.html'
    def get(self, *args, **kwargs):
        data = {}
        obj = get_object_or_404(News, slug=self.kwargs.get('slug'), is_active=True)
        data['form_news'] = NewsForm(instance=obj)
        return render(self.request, self.TEMPLATES, context=data)
    
    def post(self, *args, **kwargs):
        obj = get_object_or_404(News, slug=self.kwargs.get('slug'), is_active=True)
        form = NewsForm(self.request.POST, instance=obj)
        if form.is_valid:
            form.save()
            return redirect('news-page', slug=obj.slug)
        else:
            data['form_news'] = form
            return render(self.request, self.TEMPLATES, context=data)
