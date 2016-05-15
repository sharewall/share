from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect
from buttons_constructor.forms import ButtonsConstructorForm
from buttons_constructor.models import ButtonsConstructorModel, BtnsImages, SocialNetworks, AdvertBtnImage, Advert
from webmaster_area.models import WebmasterAreaModel
from django.contrib.auth.models import User

class ButtonsConstructorIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'buttons_constructor/index.html'
    title = 'Список ваших конструкторов'
    header = title

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):

        return HttpResponseRedirect('/buttons-constructor/create/')

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
    title = 'Конструктор'
    header = title
    
    if request.method == 'POST':
        buttons_constructor_form = ButtonsConstructorForm(data=request.POST)
        profile_user = None

        if request.user.is_staff and request.session.get('profile', False):
            profile_user = User.objects.get(pk=request.session.get('profile').get('pk'))

        if buttons_constructor_form.is_valid():

            buttons_constructor = buttons_constructor_form.save()
            cabinet_webmaster = profile_user.cabinet_webmaster if profile_user is not None else request.user.cabinet_webmaster

            buttons_constructor.cabinet_webmaster = cabinet_webmaster

            cleaned_social_networks = ''
            for s in buttons_constructor_form.cleaned_data.get('social_networks'):
                cleaned_social_networks += s + ','

            cleaned_social_networks = cleaned_social_networks[:-1]
            buttons_constructor.social_networks = cleaned_social_networks

            buttons_constructor.save()

            #Advert-isNeed
            request_need_advert = request.POST.get('advert', False) 

            wm_area_pk_post = request.POST.get('webmaster_area','')
            if wm_area_pk_post:
                if wm_area_pk_post != 'all':

                    try:
                        wm_area = WebmasterAreaModel.objects.select_related('buttons_constructor').get(pk=wm_area_pk_post, buttons_constructor__cabinet_webmaster__user=profile_user) if profile_user is not None else WebmasterAreaModel.objects.select_related('buttons_constructor').get(pk=wm_area_pk_post, buttons_constructor__cabinet_webmaster__user=request.user)

                        old_btn_const = wm_area.buttons_constructor

                        try:
                            if old_btn_const.advert.exists():
                                if request_need_advert:
                                    old_advert = Advert.objects.select_related('buttons_constructor').get(buttons_constructor__pk=old_btn_const.pk)

                                    old_advert.buttons_constructor = buttons_constructor
                                    old_advert.btn_image = AdvertBtnImage.objects.get(pk=int(request.POST.get('btn_image', 1)))
                                    old_advert.ad_type = request.POST.get('ad_type', 'SHO')
                                    old_advert.ad_allow = request.POST.get('ad_allow', 'MED')

                                    old_advert.save()
                            else:
                                if request_need_advert:
                                    new_advert = Advert.objects.create(buttons_constructor=buttons_constructor, cabinet_webmaster=cabinet_webmaster)

                                    new_advert.btn_image = AdvertBtnImage.objects.get(pk=int(request.POST.get('btn_image', 1)))
                                    new_advert.ad_type = request.POST.get('ad_type', 'SHO')
                                    new_advert.ad_allow = request.POST.get('ad_allow', 'MED')

                                    new_advert.save()
                        except:
                            pass

                        wm_area.buttons_constructor = buttons_constructor
                        wm_area.save()

                        ButtonsConstructorModel.objects.get(pk=old_btn_const.pk).delete()
                    except:
                        pass
                else:
                    wm_area_list = WebmasterAreaModel.objects.select_related('buttons_constructor').filter(buttons_constructor__cabinet_webmaster__user=profile_user) if profile_user is not None else WebmasterAreaModel.objects.select_related('buttons_constructor').filter(buttons_constructor__cabinet_webmaster__user=request.user)

                    old_btns_pk_list = []

                    try:
                        for w in wm_area_list:
                            if w.buttons_constructor.pk not in old_btns_pk_list:
                                old_btns_pk_list.append(w.buttons_constructor.pk)

                            w.buttons_constructor = buttons_constructor
                            w.save()

                        for pk in old_btns_pk_list:
                            ButtonsConstructorModel.objects.get(pk=pk).delete()
                    except:
                        pass

                #return HttpResponse(resp)
                return HttpResponseRedirect('/admin/profile/'+str(profile_user.pk)+'/?next=/') if profile_user is not None else HttpResponseRedirect('/')

    areas = None

    if request.user.is_staff and request.session.get('profile', False):
        areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'))
    
    return render(request, template_name,
    {
        'page': { 'title': title, 'header': header },
        #'buttons_constructor_form': ButtonsConstructorForm(),
        #"areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
        #'areas': list_distinct,
        'areas': areas if areas is not None else WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),
        'btns_images': BtnsImages.objects.all(),
        'social_networks': SocialNetworks.objects.all(),
        'adv_btn_image': AdvertBtnImage.objects.all()
    })
