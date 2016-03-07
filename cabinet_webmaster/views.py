from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class CabinetWebmasterIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'cabinet_webmaster/index.html'
    title = 'Cabinet webmaster'
    header = title

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
        {
            "page": { "title": self.title }
        })
