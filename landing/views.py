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
from webmaster_area.models import WebmasterAreaModel, AreaToday
#from django.views.decorators.cache import cache_page
#from django.conf import settings
#from django.contrib.auth.hashers import check_password

# not use
class LandingView(TemplateView):#LoginRequiredMixin, TemplateView):
    #login_url = '/login/' 

    template_name = 'landing/login.html'
    title = 'Sharewall'

    def get(self, request, *args, **kwargs):

        # not work change template!
        #template_name = 'webmaster_area/statistic-main.html'
        #title = 'Общая статистика'

        return render(request, self.template_name,
        {
            "page": { "title": self.title }
        })

def landing(request):
    
    if request.user.is_authenticated():
        template_name = 'webmaster_area/statistic-main.html'
        title = 'Общая статистика'
    else:
        template_name = 'landing/login.html'
        title = 'Sharewall'

    return render(request, template_name,
    {
        "page": { "title": title }
    })

@login_required
def chat(request):
    template_name = 'landing/chat.html'
    title = 'Мои тикеты'
    header = title

    if request.user.is_staff and request.session.get('profile', False):
        chats_from_user = Chat.objects.filter(user__pk=request.session.get('profile').get('pk'))
        chats_to_user = Chat.objects.filter(to_user_pk=request.session.get('profile').get('pk'))
        chats = list(chain(chats_from_user, chats_to_user))
        #chats = Chat.objects.filter(Q(user__pk=request.session.get('profile').get('pk')) or Q(to_user_pk=request.session.get('profile').get('pk')))
    else:
        chats_from_user = Chat.objects.filter(user=request.user)
        chats_to_user = Chat.objects.filter(to_user_pk=request.user.pk)
        chats = list(chain(chats_from_user, chats_to_user))
        #chats = Chat.objects.filter(Q(user=request.user) or Q(to_user_pk=request.user.pk))

    return render(request, template_name,
    {
        "page": { "title": title, "header": header },
        'chats': chats
    })

@login_required
def chat_update(request, pk):
    template_name = 'landing/chat-update.html'
    title = 'Просмотр тикета'
    header = title
    chat = None
    chatMessages = []

    if request.method == 'POST':

        #TODO: validate
        name = request.POST.get('name', request.user.username)
        email = request.POST.get('email', request.user.email)
        text = request.POST.get('text','')

        try:
            if request.user.is_staff:
                chat = Chat.objects.get(pk=pk).select_related('user')
            else:
                chat = Chat.objects.get(pk=pk, user=request.user)

            chatMessage = ChatMessage.objects.create(user=request.user, chat=chat, name=name, email=email, text=text)
            for f in request.FILES.getlist('files'):
                ChatMessageFile.objects.create(user=request.user, chat_message=chatMessage, file_store=f, file_name=f.name[-100:])
        except:
            pass

        return HttpResponseRedirect(reverse('chat-update', args=[pk]))
    
    try:
        if request.user.is_staff:
            chat = Chat.objects.get(pk=pk)
        else:
            chat = Chat.objects.get(pk=pk, user=request.user)

        header = 'Тикет #%s'%str(pk)+' (%s)'%chat.header

        tempChatMessages = ChatMessage.objects.filter(chat=chat)
        for message in tempChatMessages:
            files = ChatMessageFile.objects.filter(chat_message=message)
            chatMessages.append({'message': message, 'files': files})
    except:
        pass

    return render(request, template_name,
    {
        "page": { "title": title, "header": header },
        'chat': chat,
        'chatMessages': chatMessages
    })

@login_required
def chat_create(request):
    template_name = 'landing/chat-create.html'
    title = 'Открыть тикет'
    header = title
    users_data = []

    if request.method == 'POST':

        #TODO: validate
        header = request.POST.get('header')
        department = request.POST.get('department')
        text = request.POST.get('text')

        if request.user.is_staff:
            to_user_pk = request.POST.get('to_user_pk', False)
            if to_user_pk:
                chat = Chat.objects.create(user=request.user, to_user_pk=to_user_pk, header=header, text=text, department=department, status='ACT')
            else:
                chat = Chat.objects.create(user=request.user, header=header, text=text, department=department, status='ACT')
        else:
            chat = Chat.objects.create(user=request.user, header=header, text=text, department=department, status='ACT')

        chatMessage = ChatMessage.objects.create(user=request.user, chat=chat, name=request.user.username, email=request.user.email, text=text)

        for f in request.FILES.getlist('files'):
            ChatMessageFile.objects.create(user=request.user, chat_message=chatMessage, file_store=f, file_name=f.name[-100:])

        return HttpResponseRedirect(reverse('chat-all'))

    if request.user.is_staff:
        users_data = sorted(list(User.objects.values_list('pk', 'username')))

    return render(request, template_name,
    {
        "page": { "title": title, "header": header },
        'users_data': users_data
    })

@login_required
def admin_chat_billing(request):
    template_name = 'landing/chat.html'
    title = 'Биллинг'
    header = title

    if request.user.is_staff:
        chats = Chat.objects.filter(department='BIL')

        return render(request, template_name,
        {
            "page": { "title": title, "header": header },
            'chats': chats
        })

    return HttpResponseRedirect(reverse('landing-login'))

@login_required
def admin_chat_support(request):
    template_name = 'landing/chat.html'
    title = 'Служба поддержки'
    header = title


    if request.user.is_staff:
        chats = Chat.objects.filter(department='SUP')

        return render(request, template_name,
        {
            "page": { "title": title, "header": header },
            'chats': chats
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
def admin_wm_by_id(request):

    if request.user.is_staff:
        answer = ''
        request_pattern = request.GET.get('pattern', '')
        webmasters = []
        
        if request_pattern == '':
            webmasters = sorted(list(User.objects.all().values_list('pk', 'username')))
            answer = 'ok'
        else:
            try:
                int(request_pattern)
                temp_1 = User.objects.filter(pk__icontains=request_pattern).values_list('pk', 'username')
            except:
                temp_1 = []

            try:
                temp_2 = User.objects.filter(username__icontains=request_pattern).values_list('pk', 'username')

                webmasters = sorted(list(chain(temp_1, temp_2)))
                answer = 'ok'
            except:
                answer = 'error'

        return JsonResponse({"answer": answer, "webmasters": webmasters})

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
    title = 'Sharewall'

    request_next = request.GET.get('next', '/') # request.PATH 

    if request.method == 'POST':

        usernameoremail = request.POST.get('usernameoremail', False)
        password = request.POST.get('password', False)

        if usernameoremail and password:
            try:
                # email authenticate
                user = User.objects.get(email=usernameoremail)
                if user.check_password(password):
                    user = authenticate(username=user.username, password=password)
                else:
                    user = None
            except:
                user = None

            if user is None:
                # user authenticate
                user = authenticate(username=usernameoremail, password=password)
        else:
            user = None

        if user:
            if user.is_active:
                django_login(request, user)
                return HttpResponse("Авторизирован")
                #return HttpResponseRedirect(request_next)
            else:
                return HttpResponse("Аккаунт забанен")
                #return render(request, template_name,
                #{
                #    'error': 'User account disabled'
                #})
        else:
            return HttpResponse("Ошибка авторизации")
            #return render(request, template_name,
            #{
            #    'error': 'Invalid authenticate'
            #})
    else:
        sites = WebmasterAreaModel.objects.all().count()
        sites = int(sites*10.5)

        shares = 0
        socials = 0
        money = 0
        areaTodayList = AreaToday.objects.all()
        for a in areaTodayList:
            shares += (
                int(a.today_share_counter.split(',')[0])+
                int(a.today_share_counter.split(',')[1])+
                int(a.today_share_counter.split(',')[2])+
                int(a.today_share_counter.split(',')[3])+
                int(a.today_share_counter.split(',')[4])+
                int(a.today_share_counter.split(',')[5])+
                int(a.today_share_counter.split(',')[6])+
                int(a.today_share_counter.split(',')[7])
            )

            socials += (
                int(a.today_social_counter.split(',')[0])+
                int(a.today_social_counter.split(',')[1])+
                int(a.today_social_counter.split(',')[2])+
                int(a.today_social_counter.split(',')[3])+
                int(a.today_social_counter.split(',')[4])+
                int(a.today_social_counter.split(',')[5])+
                int(a.today_social_counter.split(',')[6])+
                int(a.today_social_counter.split(',')[7])
            )

            money += float(a.today_money)

        money = float(money*109005)

        return render(request, template_name,
        {
            "page": { "title": title },
            "stats": { "sites": sites, "shares": shares, "socials": socials, "money": money  }
        })

#@csrf_exempt
def register(request):
    template_name = 'landing/login.html'
    title = 'Sharewall'

    request_next = request.GET.get('next', '/')

    if request.method == 'POST':
        # check username
        if User.objects.filter(username=request.POST.get('username','')).count() > 0:
            return HttpResponse('Имя занятo')

        user_form = UserForm(data=request.POST)
        cabinet_webmaster_form = CabinetWebmasterForm(data={ 'wmr':'', 'mobile_phone':'', 'skype':'' })

        if user_form.is_valid() and cabinet_webmaster_form.is_valid():
            # check email
            if User.objects.filter(email=request.POST.get('email','')).count() > 0:
                return HttpResponse('E-mail занят')

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            cabinet_webmaster = cabinet_webmaster_form.save(commit=False)
            cabinet_webmaster.user = user
            cabinet_webmaster.save()

            answer = 'Регистрация успешна! Вы можете войти под именем %s'%user.username
            return HttpResponse(answer)
            #return HttpResponseRedirect(reverse('landing-login'))#, kwargs={'success':'f'}))
            #return render(request, template_name,
            #{
            #    'success': 'Success registration! You can login with {0}'.format(user.username)
            #    'success': 'Registration success'
            #})
        else:
            user_form = UserForm(user_form.cleaned_data)
            cabinet_webmaster_form = CabinetWebmasterForm(cabinet_webmaster_form.cleaned_data)
            return HttpResponse('Ошибка регистрации!')
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
