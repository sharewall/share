from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect
from buttons_constructor.forms import ButtonsConstructorForm
from buttons_constructor.models import ButtonsConstructorModel

class ButtonsConstructorIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'buttons_constructor/index.html'
    title = 'Buttons constructor'
    header = 'Список ваших конструкторов'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/buttons-constructor/create/')
        '''
        return render(request, self.template_name,
        {
            "constructors": ButtonsConstructorModel.objects.filter(cabinet_webmaster=request.user.cabinet_webmaster),
            "page": { "title": self.title, 'header': self.header }
        })
        '''

@login_required
def delete(request, pk):
    try:
        ButtonsConstructorModel.objects.get(pk=pk).delete()
    except Exception as inst:
        pass
    return HttpResponseRedirect('/buttons-constructor/')

@login_required
def update(request, pk):
    template_name = 'buttons_constructor/update.html'
    title = 'Update buttons constructor'
    request_instance = None
    try:
        request_instance = ButtonsConstructorModel.objects.get(pk=pk)
    except Exception as inst:
        pass
    if request_instance:
        request_form_data = {
            'name_constructor': request_instance.name_constructor,
            'with_counter': request_instance.with_counter,
            'page_url': request_instance.page_url,
            'page_title': request_instance.page_title,
            'page_description': request_instance.page_description,
            'location_buttons': request_instance.location_buttons,
            'social_networks': request_instance.social_networks.split(','), #('vk','fb')
            'btns_images': request_instance.btns_images
        }
        buttons_constructor_form = ButtonsConstructorForm(data=request_form_data, instance=request_instance, auto_id=False)#, initial={'social_networks': ['vk','fb']}
        header = request_instance.name_constructor
        if request.method == 'POST':
            buttons_constructor_form = ButtonsConstructorForm(data=request.POST, instance=request_instance)
            if buttons_constructor_form.is_valid():
                buttons_constructor = buttons_constructor_form.save(commit=False)
                #buttons_constructor.cabinet_webmaster = request.user.cabinet_webmaster
                cleaned_social_networks = ''
                for s in buttons_constructor_form.cleaned_data.get('social_networks'):
                    cleaned_social_networks += s + ','
                cleaned_social_networks = cleaned_social_networks[:-1]
                buttons_constructor.social_networks = cleaned_social_networks
                buttons_constructor.save()
                return HttpResponseRedirect('/buttons-constructor/')
                #return render(request, template_name,
                #{
                    #'success': 'Buttons constructor created'
                #})
            else:
                buttons_constructor_form = ButtonsConstructorForm(buttons_constructor_form.cleaned_data)
                return render(request, template_name,
                {
                    'page': { 'title': title, 'header': header },
                    'error': buttons_constructor_form.errors,
                    'buttons_constructor_form': buttons_constructor_form
                })
        else:
            #return HttpResponseRedirect('/buttons-constructor/')
            return render(request, template_name,
            {
                'pk': pk,
                'page': { 'title': title, 'header': header },
                'buttons_constructor_form': buttons_constructor_form
            })
    else:
        return HttpResponseRedirect('/buttons-constructor/')

@login_required
def create(request):
    template_name = 'buttons_constructor/create.html'
    title = 'Create buttons constructor'
    header = 'Конструктор'
    if request.method == 'POST':
        buttons_constructor_form = ButtonsConstructorForm(data=request.POST)
        if buttons_constructor_form.is_valid():
            buttons_constructor = buttons_constructor_form.save()
            buttons_constructor.cabinet_webmaster = request.user.cabinet_webmaster
            cleaned_social_networks = ''
            for s in buttons_constructor_form.cleaned_data.get('social_networks'):
                cleaned_social_networks += s + ','
            cleaned_social_networks = cleaned_social_networks[:-1]
            buttons_constructor.social_networks = cleaned_social_networks
            buttons_constructor.save()
            return HttpResponseRedirect('/buttons-constructor/')
            #return render(request, template_name,
            #{
                #'success': 'Buttons constructor created'
            #})
        else:
            buttons_constructor_form = ButtonsConstructorForm(buttons_constructor_form.cleaned_data)
            return render(request, template_name,
            {
                'page': { 'title': title, 'header': header },
                'error': buttons_constructor_form.errors,
                'buttons_constructor_form': buttons_constructor_form
            })
    else:
        #return HttpResponseRedirect('/buttons-constructor/')
        return render(request, template_name,
        {
            'page': { 'title': title, 'header': header },
            'buttons_constructor_form': ButtonsConstructorForm()
        })


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

