from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from landing.forms import UserForm, CabinetWebmasterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.core.urlresolvers import reverse
#from django.views.decorators.cache import cache_page
#from django.contrib.auth.models import User
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
        })

@login_required
def admin_webmasters(request):
    template_name = 'landing/admin-webmasters.html'
    title = 'Вебмастера'
    header = title

    if request.user.is_staff:
        return render(request, template_name,
        {
            "page": { "title": title, "header": header }
        })
    return HttpResponseRedirect('/login/')

@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')

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
        return HttpResponseRedirect('/login/')    
        #if not 'user_form' in locals():
            #user_form = UserForm()
        #if not 'cabinet_webmaster_form' in locals():
            #cabinet_webmaster_form = CabinetWebmasterForm()
