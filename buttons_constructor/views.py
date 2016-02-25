from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

class ButtonsConstructorIndexView(TemplateView):
    template_name = 'buttons_constructor/index.html'
    title = 'Index'
    header = title
    # records = LandingModel.objects.all()
    # def get_context_data(self, **kwargs):
        # records = LandingModel.objects.all()
        # context = dict(records=records)
        # return context

#class LandingAboutView(TemplateView):
    #template_name = 'landing/about.html'

    #def get_context_data(self, **kwargs):
        #record = get_object_or_404(LandingModel, pk=kwargs['pk'])
        #context = dict(record=record, header='About %s' % record.title, title='About' + record.title)
        #return context

