from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from landing.forms import UserForm, CabinetWebmasterForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.core.urlresolvers import reverse
from cabinet_webmaster.models import CabinetWebmasterModel, Chat, ChatMessage, ChatMessageFile
from django.contrib.auth.models import User
from itertools import chain
from django.db.models import Q
from django.core import serializers
from webmaster_area.models import WebmasterAreaModel
#from django.views.decorators.cache import cache_page
#from django.conf import settings
#from django.contrib.auth.hashers import check_password

class LandingView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    #template_name = 'landing/index.html'
    template_name = 'webmaster_area/statistic-main.html'
    title = 'Главная'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
        {
            "page": { "title": self.title }
            #"profile": request.session.get('profile')
        })

@login_required
def chat(request):
    template_name = 'landing/chat.html'
    title = 'Мои тикеты'
    header = title

    chats = Chat.objects.filter(user=request.user)

    return render(request, template_name,
    {
        "page": { "title": title, "header": header },
        'chats': chats
    })

@login_required
def chat_create(request):
    template_name = 'landing/chat-create.html'
    title = 'Открыть тикет'
    header = title

    if request.method == 'POST':

        #TODO: validate
        header = request.POST.get('header')
        department = request.POST.get('department')
        text = request.POST.get('text')

        chat = Chat.objects.create(user=request.user, header=header, text=text, department=department, status='ACT')

        chatMessage = ChatMessage.objects.create(user=request.user, chat=chat, name=request.user.username, text=text)

        for f in request.FILES.getlist('files'):
            ChatMessageFile.objects.create(user=request.user, chat_message=chatMessage, file_store=f)

        return HttpResponseRedirect(reverse('chat-all'))

    return render(request, template_name,
    {
        "page": { "title": title, "header": header }
    })

@login_required
def admin_chat_billing(request):
    template_name = 'landing/chat.html'
    title = 'Биллинг'
    header = title

    if request.user.is_staff:
        return render(request, template_name,
        {
            "page": { "title": title, "header": header }
        })

    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_chat_support(request):
    template_name = 'landing/chat.html'
    title = 'Служба поддержки'
    header = title

    if request.user.is_staff:
        return render(request, template_name,
        {
            "page": { "title": title, "header": header }
        })

    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_webmasters(request):
    template_name = 'landing/admin-webmasters.html'
    title = 'Вебмастера'
    header = title

    if request.user.is_staff:
        get_query_filter = request.GET.get('q')
        all_cabinets = []

        if get_query_filter:
            try:
                int(get_query_filter)
                temp_1 = CabinetWebmasterModel.objects.select_related("user").filter(pk__exact=get_query_filter)
            except:
                temp_1 = []

            #temp_2 = CabinetWebmasterModel.objects.select_related("user").filter(user__username__icontains=get_query_filter)
            #temp_3 = CabinetWebmasterModel.objects.select_related("user").filter(user__email__icontains=get_query_filter)
            temp_2 = CabinetWebmasterModel.objects.select_related("user").filter(Q(user__username__icontains=get_query_filter) | Q(user__email__icontains=get_query_filter))

            all_cabinets = list(chain(temp_1, temp_2))
        else:
            all_cabinets = CabinetWebmasterModel.objects.select_related("user")

        return render(request, template_name,
        {
            "page": { "title": title, "header": header },
            "all_cabinets": all_cabinets,
            "q": get_query_filter
        })

    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_area_by_id(request):

    if request.user.is_staff and request.GET.get('wmid', False):
        answer = ''
        request_wmid = request.GET.get('wmid')
        areas = []

        try:
            areas = sorted(list(WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user__pk__exact=request_wmid).values_list('name_area', flat=True)))
            answer = 'ok'
        except:
            answer = 'error'

        return JsonResponse({"answer": answer, "areas": areas})

    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_change_status(request):

    if request.user.is_staff:
        answer = ''
        status = None

        cabinet_pk = request.GET.get('id')
        status = request.GET.get('status')

        try:
            if cabinet_pk:
                user = User.objects.get(cabinet_webmaster__pk=cabinet_pk)
                user.is_active = True if status == 'true' else False
                user.save()
                answer = 'ok'
            else:
                answer = 'error, no id'
        except:
            answer = 'error'

        return JsonResponse({"answer": answer, "status": status})

    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_profile(request, pk):

    if request.user.is_staff:
        try:
            user = User.objects.select_related('cabinet_webmaster').get(pk=pk)
            request.session['profile'] = {
                'pk': user.pk, 
                'username': user.username, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email, 
                'wmr': user.cabinet_webmaster.wmr, 
                'skype': user.cabinet_webmaster.skype, 
                'mobile_phone': user.cabinet_webmaster.mobile_phone, 
                'money': user.cabinet_webmaster.money,
                'is_active': user.is_active,
                'is_staff': user.is_staff
            }
        except:
            return HttpResponseRedirect('/admin/webmasters')

        request_next = request.GET.get('next', '/') # request.PATH 
        return HttpResponseRedirect(request_next)
    
    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_profile_clear(request):

    if request.user.is_staff:
        #request.session['profile'] = None
        del request.session['profile']
        return HttpResponseRedirect('/admin/webmasters')
    
    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def logout(request):
    django_logout(request)

    return HttpResponseRedirect(reverse('landing-login'))

#@csrf_exempt
@ensure_csrf_cookie
def login(request):
    template_name = 'landing/login.html'
    title = 'Авторизация'

    request_next = request.GET.get('next', '/') # request.PATH 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                django_login(request, user)
                return HttpResponse("Login success")
                #return HttpResponseRedirect(request_next)
            else:
                return HttpResponse("Account disabled")
                #return render(request, template_name,
                #{
                #    'error': 'User account disabled'
                #})
        else:
            return HttpResponse("Invalid authenticate")
            #return render(request, template_name,
            #{
            #    'error': 'Invalid authenticate'
            #})
    else:
        return render(request, template_name,
        {
            "page": { "title": title }
        })

#@csrf_exempt
def register(request):
    template_name = 'landing/login.html'
    title = 'Register'

    request_next = request.GET.get('next', '/')

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        cabinet_webmaster_form = CabinetWebmasterForm(data={ 'wmr':'', 'mobile_phone':'', 'skype':'' })
        if user_form.is_valid() and cabinet_webmaster_form.is_valid():
            #TODO: check email
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            cabinet_webmaster = cabinet_webmaster_form.save(commit=False)
            cabinet_webmaster.user = user
            cabinet_webmaster.save()
            answer = 'Register success! You can login now with %s'%user.username
            return HttpResponse(answer)
            #return HttpResponseRedirect(reverse('landing-login'))#, kwargs={'success':'f'}))
            #return render(request, template_name,
            #{
            #    'success': 'Success registration! You can login with {0}'.format(user.username)
            #    'success': 'Registration success'
            #})
        else:
            user_form = UserForm(user_form.cleaned_data)
            if cabinet_webmaster_form.is_valid():
                pass
            cabinet_webmaster_form = CabinetWebmasterForm(cabinet_webmaster_form.cleaned_data)
            return HttpResponse('Registration error')
            #return render(request, template_name,
            #{
            #    'error': 'Registration error',
            #    'user_form': user_form,
            #    'cabinet_webmaster_form': cabinet_webmaster_form
            #})
    else:
        return HttpResponseRedirect(reverse('landing-login'))
        #if not 'user_form' in locals():
            #user_form = UserForm()
        #if not 'cabinet_webmaster_form' in locals():
            #cabinet_webmaster_form = CabinetWebmasterForm()
