from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from landing.forms import UserForm, CabinetWebmasterForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

class CabinetWebmasterIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'cabinet_webmaster/index.html'
    title = 'Настройки'
    header = title

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
        {
            "page": { "title": self.title }
        })
        
@login_required
def settings(request):
    if request.method == 'POST':
        answer = ''
        request_user = {}
        request_user['username'] = request.user.get_username()
        request_user['email'] = request.user.email
        request_user['password'] = request.user.password
        request_user['first_name'] = request.user.first_name
        request_user['last_name'] = request.user.last_name
        request_post = {}
        request_post['password'] = request.POST.get('password')
        request_post['new_password'] = request.POST.get('new_password')
        request_post['money'] = request.POST.get('money')
        request_post['wmr'] = request.POST.get('wmr')
        request_post['mobile_phone'] = request.POST.get('mobile_phone')
        request_post['skype'] = request.POST.get('skype')
        request_post['first_name'] = request.POST.get('first_name')
        request_post['last_name'] = request.POST.get('last_name')
        request_post['email'] = request.POST.get('email')

        user_form = UserForm(data=request_user, instance=request.user)
        if(user_form.is_valid()):
            user = user_form.save(commit=False)
            if request.POST.get('delete_account') and request.POST.get('delete_account') == 'УДАЛИТЬ':
                user.is_active = False
                user.save()
                django_logout(request)
                answer = 'УДАЛИТЬ'
            elif request_post.get('password') and request.user.check_password(request_post.get('password')):
                user.set_password(request_post.get('new_password'))
                user.save()
                answer = 'PASS'
            elif request_post.get('first_name'):
                user.first_name = request_post.get('first_name')
                user.save()
                answer = user.first_name
            elif request_post.get('last_name'):
                user.last_name = request_post.get('last_name')
                user.save()
                answer = user.last_name
            elif request_post.get('email'):
                user.email = request_post.get('email')
                user.save()
                answer = user.email
            elif request_post.get('wmr'):
                user.cabinet_webmaster.wmr = request_post.get('wmr')
                user.cabinet_webmaster.save()
                answer = user.cabinet_webmaster.wmr
            elif request_post.get('skype'):
                user.cabinet_webmaster.skype = request_post.get('skype')
                user.cabinet_webmaster.save()
                answer = user.cabinet_webmaster.skype
            elif request_post.get('mobile_phone'):
                user.cabinet_webmaster.mobile_phone = request_post.get('mobile_phone')
                user.cabinet_webmaster.save()
                answer = user.cabinet_webmaster.mobile_phone
        else:
            answer = 'BAD USER-FORM'

        return HttpResponse(answer)
    else:
        return HttpResponseRedirect('/cabinet-webmaster/')
