from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

class CabinetWebmasterIndexView(TemplateView):
    template_name = 'cabinet_webmaster/index.html'
    title = 'Index'
    header = title
