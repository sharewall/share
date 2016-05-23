import datetime, json, os, re, sys, requests
import urllib.request, uuid, urllib3, json
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from webmaster_area.models import WebmasterAreaModel, PageDetail, AreaToday
from webmaster_area.forms import WebmasterAreaForm, AreaCategory
from buttons_constructor.models import BtnsImages, AdvertBtnImage, Advert, SocialNetworks, ButtonsConstructorModel
from cabinet_webmaster.models import CabinetWebmasterModel
from bs4 import BeautifulSoup
from itertools import chain
from django.db.models import Q, Sum
from django.core.validators import URLValidator

class WebmasterAreaIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'webmaster_area/index.html'
    title = 'Площадки'
    header = title

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        areas = None

        if request.user.is_staff and request.session.get('profile', False):
            areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'))

        return render(request, self.template_name,
        {
            'areas': areas if areas is not None else WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),
            #"areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
            "page": { "title": self.title, 'header': self.header },
            "ad_type": "Нормальный,Для взрослых",
            "area_category": AreaCategory.objects.all()
        })

@login_required
def statistic(request):
    template_name = 'webmaster_area/statistic.html'
    title = 'Статистика'
    header = 'Статистика'
    areas = None
    users_data = []

    if request.user.is_staff:
        #users = User.objects.all()
        users_data = sorted(list(User.objects.values_list('pk', 'username')))
        #for u in users:
        #    users_data[u[0]]=u[1]

    if request.user.is_staff and request.session.get('profile', False):
        areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'))

    return render(request, template_name,
    {
        'users_data': users_data,
        'areas': areas if areas is not None else WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),
        #'areas': WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),
        'page': { 'title': title, 'header': header }
    })

def updateServer(request):
    answer = "Answer= "
    areas = WebmasterAreaModel.objects.all()

    for area in areas:
        answer = answer + area.name_area + ": "
        area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        if area_per_day_list.last():
            last_day = area_per_day_list.last()

            if datetime.datetime.now().date() == last_day.date:
                page_detail_list = PageDetail.objects.filter(webmaster_area=area)            

                last_day.today_social_counter = ''
                temp_all_social_counters = [0,0,0,0,0,0,0,0]

                last_day.today_share_counter = ''
                temp_all_share_counters = [0,0,0,0,0,0,0,0]

                for pd in page_detail_list:
                    temp_social_counter = [int(s) for s in pd.total_social_counter.split(',')]
                    index=0

                    temp_share_counter = [int(s) for s in pd.total_share_counter.split(',')]
                    index2=0

                    for i,i2 in zip(temp_all_social_counters, temp_social_counter):
                        temp_all_social_counters[index]=(i+i2)
                        index+=1

                    for i,i2 in zip(temp_all_share_counters, temp_share_counter):
                        temp_all_share_counters[index2]=(i+i2)
                        index2+=1

                for i in temp_all_social_counters:
                    last_day.today_social_counter += str(i) + ','

                for i in temp_all_share_counters:
                    last_day.today_share_counter += str(i) + ','

                last_day.today_social_counter = last_day.today_social_counter[:-1]
                answer = answer + last_day.today_social_counter + "; "

                last_day.today_share_counter = last_day.today_share_counter[:-1]
                answer = answer + last_day.today_share_counter + ". "

                last_day.save()


    return HttpResponse(answer)

@login_required
def detailmain(request):
    template_name = 'webmaster_area/detail-main.html'
    
    dates = []
    shares = []
    socials = []
    shows = []
    clicks = []
    money = []
    dates_range_start = None
    dates_range_end = None
    isEmpty = True
    temp_statistic = {
        'shares': 0,
        'socials': 0,
        'shows': 0,        
        'clicks': 0,        
        'money': 0
    }
    statistic = {
        'shares': 0,        
        'socials': 0,        
        'shows': 0,        
        'clicks': 0,        
        'money': 0
    }
    for_1 = False # Not all
    area_first = None
    areas = []
    temp_area_per_day_statistic = []

    if request.user.is_staff and request.GET.get('for', False) and request.GET.get('for') == '1':
        #areas = WebmasterAreaModel.objects.all()
        for_1 = True
        area_first = WebmasterAreaModel.objects.first()
        #statistic['money'] = CabinetWebmasterModel.objects.aggregate(Sum('money')).get('money__sum', 0)
    elif request.user.is_staff and request.session.get('profile', False):
        areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'))
    else:
        areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user)
    
    if area_first or areas.first():
        isEmpty = False

    try:
        request_dateRange = request.GET.get('daterange').split(' - ')
        dates_range_start = datetime.datetime.strptime(request_dateRange[0], "%d.%m.%Y").date()
        dates_range_end = datetime.datetime.strptime(request_dateRange[1], "%d.%m.%Y").date()
    except:
        temp_areaTodayList = None

        if for_1 and area_first is not None:
            temp_first_area_today = AreaToday.objects.filter(webmaster_area=area_first)
            if temp_first_area_today.first():
                dates_range_start = temp_first_area_today.date
            else:
                dates_range_start = datetime.datetime.now().date()

            dates_range_end = datetime.datetime.now().date()
        elif not isEmpty:
            #temp_areaTodayList = AreaToday.objects.filter(Q(webmaster_area=areas.first()) and Q(webmaster_area=areas.last()))#and last for correct date range
            temp_areaTodayList = AreaToday.objects.filter(webmaster_area=areas.first())

        if temp_areaTodayList is not None and temp_areaTodayList.first():
            temp_areaToday = temp_areaTodayList.first()
            dates_range_start = temp_areaToday.date#.strftime("%d.%m.%Y")

            dates_range_end = datetime.datetime.now().date()
        else:
            dates_range_start = datetime.datetime.now().date()
            dates_range_end = datetime.datetime.now().date()

    #TODO: If for all, then vehicle:
    if for_1:
        areas = [0,]

    for area in areas:

        temp_statistic['shares'] = 0
        temp_statistic['socials'] = 0

        #Adv
        temp_statistic['shows'] = temp_statistic.get('shows', 0)
        temp_statistic['clicks'] = temp_statistic.get('clicks', 0)
        temp_statistic['money'] = temp_statistic.get('money', 0)

        if for_1:
            area_per_day_list = AreaToday.objects.all()#.select_related('webmaster_area')
        elif dates_range_start and dates_range_end:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area, date__range=(dates_range_start, dates_range_end))#["2016-04-11", "2016-04-12"])
        else:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        if not for_1 and area_per_day_list.last():
            last_day = area_per_day_list.last()

            #TODO: need update Adv
            if datetime.datetime.now().date() == last_day.date:
                page_detail_list = PageDetail.objects.filter(webmaster_area=area)            

                last_day.today_social_counter = ''
                temp_all_social_counters = [0,0,0,0,0,0,0,0]

                last_day.today_share_counter = ''
                temp_all_share_counters = [0,0,0,0,0,0,0,0]

                for pd in page_detail_list:
                    temp_social_counter = [int(s) for s in pd.total_social_counter.split(',')]
                    index=0

                    temp_share_counter = [int(s) for s in pd.total_share_counter.split(',')]
                    index2=0

                    for i,i2 in zip(temp_all_social_counters, temp_social_counter):
                        temp_all_social_counters[index]=(i+i2)
                        index+=1

                    for i,i2 in zip(temp_all_share_counters, temp_share_counter):
                        temp_all_share_counters[index2]=(i+i2)
                        index2+=1

                for i in temp_all_social_counters:
                    last_day.today_social_counter += str(i) + ','

                for i in temp_all_share_counters:
                    last_day.today_share_counter += str(i) + ','

                last_day.today_social_counter = last_day.today_social_counter[:-1]

                last_day.today_share_counter = last_day.today_share_counter[:-1]

                last_day.save()

        for a in area_per_day_list:
            temp_areaPDay_date = a.date.strftime("%d.%m")

            temp_today_share_counter = (
                int(a.today_share_counter.split(',')[0])+
                int(a.today_share_counter.split(',')[1])+
                int(a.today_share_counter.split(',')[2])+
                int(a.today_share_counter.split(',')[3])+
                int(a.today_share_counter.split(',')[4])+
                int(a.today_share_counter.split(',')[5])+
                int(a.today_share_counter.split(',')[6])+
                int(a.today_share_counter.split(',')[7])
            )

            temp_today_social_counter = (
                int(a.today_social_counter.split(',')[0])+
                int(a.today_social_counter.split(',')[1])+
                int(a.today_social_counter.split(',')[2])+
                int(a.today_social_counter.split(',')[3])+
                int(a.today_social_counter.split(',')[4])+
                int(a.today_social_counter.split(',')[5])+
                int(a.today_social_counter.split(',')[6])+
                int(a.today_social_counter.split(',')[7])
            )

            #Adv
            temp_today_shows_counter = int(a.today_show_counter)
            temp_today_clicks_counter = int(a.today_click_counter)
            temp_today_money_counter = float(a.today_money)

            if for_1:
                try:
                    temp_index = next(index for (index, d) in enumerate(temp_area_per_day_statistic) if d['date'] == a.date)

                    temp_area_per_day_statistic[temp_index]['share'] += temp_today_share_counter
                    temp_area_per_day_statistic[temp_index]['social'] += temp_today_social_counter

                    #Adv
                    temp_area_per_day_statistic[temp_index]['shows'] += temp_today_shows_counter
                    temp_area_per_day_statistic[temp_index]['clicks'] += temp_today_clicks_counter
                    temp_area_per_day_statistic[temp_index]['money'] += temp_today_money_counter
                except:
                    temp_area_per_day_statistic.append({
                        #'pk' : a.webmaster_area.pk,
                        'date' : a.date,
                        'share' : temp_today_share_counter,
                        'social' : temp_today_social_counter,
                        #Adv
                        'shows': temp_today_shows_counter,
                        'clicks': temp_today_clicks_counter,
                        'money': temp_today_money_counter
                    })
            else:
                if temp_today_share_counter > temp_statistic['shares']:
                    temp_statistic['shares'] = temp_today_share_counter

                if temp_today_social_counter > temp_statistic['socials']:
                    temp_statistic['socials'] = temp_today_social_counter

                #Adv
                #if temp_today_shows_counter > temp_statistic['shows']:
                temp_statistic['shows'] += temp_today_shows_counter

                #if temp_today_clicks_counter > temp_statistic['clicks']:
                temp_statistic['clicks'] += temp_today_clicks_counter

                #if temp_today_money_counter > temp_statistic['money']:
                temp_statistic['money'] += temp_today_money_counter

            if not temp_areaPDay_date in dates:
                dates.append(temp_areaPDay_date)
                shares.append(temp_today_share_counter)
                socials.append(temp_today_social_counter)
                #Adv
                shows.append(temp_today_shows_counter)
                clicks.append(temp_today_clicks_counter)
                money.append(temp_today_money_counter)
            else:
                shares[dates.index(temp_areaPDay_date)] += temp_today_share_counter
                socials[dates.index(temp_areaPDay_date)] += temp_today_social_counter
                #Adv
                shows[dates.index(temp_areaPDay_date)] += temp_today_shows_counter
                clicks[dates.index(temp_areaPDay_date)] += temp_today_clicks_counter
                money[dates.index(temp_areaPDay_date)] += temp_today_money_counter

        #TODO: save for each area
        if not for_1:
            statistic['shares'] += temp_statistic['shares']
            statistic['socials'] += temp_statistic['socials']
            #Adv
            statistic['shows'] += temp_statistic['shows']
            statistic['clicks'] += temp_statistic['clicks']
            statistic['money'] += temp_statistic['money']
        else:
            shows = []
            clicks = []
            money = []

            for share, social, showsT, clicksT, moneyT in [[ t['share'], t['social'], t['shows'], t['clicks'], t['money'] ] for t in temp_area_per_day_statistic]:
                if share > statistic['shares']:
                    statistic['shares'] = share
                if social > statistic['socials']:
                    statistic['socials'] = social
                #Adv
                shows.append(showsT)
                clicks.append(clicksT)
                money.append(moneyT)

                statistic['shows'] += showsT
                statistic['clicks'] += clicksT
                statistic['money'] += moneyT

    return render(request, template_name,
    {
        'temp_area_per_day_statistic': temp_area_per_day_statistic,
        'statistic': statistic,
        'isEmpty': isEmpty,
        'dates_range_start': dates_range_start.strftime("%d.%m.%Y"),
        'dates_range_end': dates_range_end.strftime("%d.%m.%Y"),
        'dates': dates,
        'shows': shows,
        'shares': shares,
        'socials': socials,
        'clicks': clicks,
        'money': money
    })

@login_required
def detailadvert(request, name):
    template_name = 'webmaster_area/detail-advert.html'
    title = name
    header = name
    
    dates = []
    shows = []
    clicks = []
    money = []
    dates_range_start = None
    dates_range_end = None
    statistic = {
        'shows': 0,        
        'clicks': 0,        
        'money': 0,        
    }

    try:
        if request.user.is_staff and request.GET.get('wmid', False):
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user__pk__exact=request.GET.get('wmid'), name_area=name)
        elif request.user.is_staff and request.session.get('profile', False):
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'), name_area=name)
        else:
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)
    except:
        area = None

    if area:
        area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        try:
            request_dateRange = request.GET.get('daterange').split(' - ')
            dates_range_start = datetime.datetime.strptime(request_dateRange[0], "%d.%m.%Y").date()
            dates_range_end = datetime.datetime.strptime(request_dateRange[1], "%d.%m.%Y").date()
        except:
            if area_per_day_list.first():
                temp_areaToday = area_per_day_list.first()
                dates_range_start = temp_areaToday.date
                temp_areaToday = area_per_day_list.last()
                dates_range_end = temp_areaToday.date
            else:
                dates_range_start = datetime.datetime.now().date()
                dates_range_end = datetime.datetime.now().date()

        if dates_range_start and dates_range_end:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area, date__range=(dates_range_start, dates_range_end))

        for a in area_per_day_list:
            dates.append(a.date.strftime("%d.%m"))
            #adv
            temp_show = int(a.today_show_counter)
            temp_click = int(a.today_click_counter)
            temp_money = float(a.today_money)

            shows.append(temp_show)
            clicks.append(temp_click)
            money.append(temp_money)

            statistic['shows'] += temp_show
            statistic['clicks'] += temp_click
            statistic['money'] += temp_money

        return render(request, template_name,
        {
            'statistic': statistic,
            'dates_range_start': dates_range_start.strftime("%d.%m.%Y"),
            'dates_range_end': dates_range_end.strftime("%d.%m.%Y"),
            'page': { 'title': title, 'header': header },
            'dates': dates,
            'shows': shows,
            'clicks': clicks,
            'money': money
        })
    else:
        return HttpResponseRedirect('/webmaster-area/detail-error/')

@login_required
def detailsocial(request, name):
    template_name = 'webmaster_area/detail-social.html'
    title = name
    header = name
    
    dates = []
    todayVK = []
    todayFB = []
    todayTW = []
    todayOD = []
    todayGP = []
    todayMA = []
    todayLI = []
    todayLJ = []
    dates_range_start = None
    dates_range_end = None
    statistic = {
        'vk': 0,        
        'fb': 0,        
        'tw': 0,        
        'od': 0,        
        'gp': 0,        
        'ma': 0,        
        'li': 0,        
        'lj': 0,
        'all': 0
    }

    try:
        if request.user.is_staff and request.GET.get('wmid', False):
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user__pk__exact=request.GET.get('wmid'), name_area=name)
        elif request.user.is_staff and request.session.get('profile', False):
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'), name_area=name)
        else:
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)
    except:
        area = None

    #area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)

    if area:
        area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        if area_per_day_list.last():
            last_day = area_per_day_list.last()

            if datetime.datetime.now().date() == last_day.date:
                page_detail_list = PageDetail.objects.filter(webmaster_area=area)            
                last_day.today_social_counter = ''
                temp_all_social_counters = [0,0,0,0,0,0,0,0]

                for pd in page_detail_list:
                    temp_social_counter = [int(s) for s in pd.total_social_counter.split(',')]
                    index=0

                    for i,i2 in zip(temp_all_social_counters, temp_social_counter):
                        temp_all_social_counters[index]=(i+i2)
                        index+=1

                for i in temp_all_social_counters:
                    last_day.today_social_counter += str(i) + ','

                last_day.today_social_counter = last_day.today_social_counter[:-1]
                last_day.save()

        try:
            request_dateRange = request.GET.get('daterange').split(' - ')
            dates_range_start = datetime.datetime.strptime(request_dateRange[0], "%d.%m.%Y").date()
            dates_range_end = datetime.datetime.strptime(request_dateRange[1], "%d.%m.%Y").date()
        except:
            if area_per_day_list.first():
                temp_areaToday = area_per_day_list.first()
                dates_range_start = temp_areaToday.date
                temp_areaToday = area_per_day_list.last()
                dates_range_end = temp_areaToday.date
            else:
                dates_range_start = datetime.datetime.now().date()
                dates_range_end = datetime.datetime.now().date()

        if dates_range_start and dates_range_end:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area, date__range=(dates_range_start, dates_range_end))

        for a in area_per_day_list:
            dates.append(a.date.strftime("%d.%m"))

            temp = int(a.today_social_counter.split(',')[0])
            todayVK.append(temp)
            if temp > statistic['vk']:
                statistic['vk'] = temp

            temp = int(a.today_social_counter.split(',')[1])
            todayFB.append(temp)
            if temp > statistic['fb']:
                statistic['fb'] = temp

            temp = int(a.today_social_counter.split(',')[2])
            todayTW.append(temp)
            if temp > statistic['tw']:
                statistic['tw'] = temp

            temp = int(a.today_social_counter.split(',')[3])
            todayOD.append(temp)
            if temp > statistic['od']:
                statistic['od'] = temp

            temp = int(a.today_social_counter.split(',')[4])
            todayGP.append(temp)
            if temp > statistic['gp']:
                statistic['gp'] = temp

            temp = int(a.today_social_counter.split(',')[5])
            todayMA.append(temp)
            if temp > statistic['ma']:
                statistic['ma'] = temp

            temp = int(a.today_social_counter.split(',')[6])
            todayLI.append(temp)
            if temp > statistic['li']:
                statistic['li'] = temp

            temp = int(a.today_social_counter.split(',')[7])
            todayLJ.append(temp)
            if temp > statistic['lj']:
                statistic['lj'] = temp

        statistic['all'] = statistic['vk'] + statistic['fb'] + statistic['tw'] + statistic['od'] + statistic['gp'] + statistic['ma'] + statistic['li'] + statistic['lj']

        return render(request, template_name,
        {
            'statistic': statistic,
            'dates_range_start': dates_range_start.strftime("%d.%m.%Y"),
            'dates_range_end': dates_range_end.strftime("%d.%m.%Y"),
            'page': { 'title': title, 'header': header },
            'dates': dates,
            'todayVK': todayVK,
            'todayFB': todayFB,
            'todayTW': todayTW,
            'todayOD': todayOD,
            'todayGP': todayGP,
            'todayMA': todayMA,
            'todayLI': todayLI,
            'todayLJ': todayLJ
        })
    else:
        return HttpResponseRedirect('/webmaster-area/detail-error/')

@login_required
def detail_error(request):
    template_name = 'webmaster_area/detail-social.html'
    title = "Ошибка"
    header = title

    return render(request, template_name,
    {
        'page': { 'title': title, 'header': header }
    })

@login_required
def detail(request, name):
    template_name = 'webmaster_area/detail.html'
    title = name
    header = name
    
    dates = []
    todayVK = []
    todayFB = []
    todayTW = []
    todayOD = []
    todayGP = []
    todayMA = []
    todayLI = []
    todayLJ = []
    dates_range_start = None
    dates_range_end = None
    statistic = {
        'vk': 0,        
        'fb': 0,        
        'tw': 0,        
        'od': 0,        
        'gp': 0,        
        'ma': 0,        
        'li': 0,        
        'lj': 0,
        'all': 0
    }
    list_page_detail = []

    try:
        if request.user.is_staff and request.GET.get('wmid', False):
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user__pk__exact=request.GET.get('wmid'), name_area=name)
        elif request.user.is_staff and request.session.get('profile', False):
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user__pk__exact=request.session.get('profile').get('pk'), name_area=name)
        else:
            area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)
    except:
        area = None

    #area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)
    
    if area:
        area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        if area_per_day_list.last():
            last_day = area_per_day_list.last()

            #TODO: list_page_detail
            page_detail_list = PageDetail.objects.filter(webmaster_area=area)            
            for pd in page_detail_list:
                temp_total_share_counter = 0
                temp_total_social_counter = 0

                for s in pd.total_share_counter.split(','):
                    temp_total_share_counter += int(s)
                for s in pd.total_social_counter.split(','):
                    temp_total_social_counter += int(s)

                list_page_detail.append({
                    'title':pd.title,
                    'url':pd.url,
                    'sharing':temp_total_share_counter,
                    'traffic':temp_total_social_counter,
                    'sharing_detail':pd.total_share_counter,
                    'traffic_detail':pd.total_social_counter
                    })

            #TODO: move sort to client
            #sorted(list_page_detail, key=lambda k: k['sharing'], reverse=True)

            if datetime.datetime.now().date() == last_day.date:
                #page_detail_list = PageDetail.objects.filter(webmaster_area=area)            
                last_day.today_share_counter = ''
                temp_all_share_counters = [0,0,0,0,0,0,0,0]

                for pd in page_detail_list:
                    temp_share_counter = [int(s) for s in pd.total_share_counter.split(',')]
                    index=0

                    for i,i2 in zip(temp_all_share_counters, temp_share_counter):
                        temp_all_share_counters[index]=(i+i2)
                        index+=1

                for i in temp_all_share_counters:
                    last_day.today_share_counter += str(i) + ','

                last_day.today_share_counter = last_day.today_share_counter[:-1]
                last_day.save()

        try:
            request_dateRange = request.GET.get('daterange').split(' - ')
            dates_range_start = datetime.datetime.strptime(request_dateRange[0], "%d.%m.%Y").date()
            dates_range_end = datetime.datetime.strptime(request_dateRange[1], "%d.%m.%Y").date()
        except:
            if area_per_day_list.first():
                temp_areaToday = area_per_day_list.first()
                dates_range_start = temp_areaToday.date
                temp_areaToday = area_per_day_list.last()
                dates_range_end = temp_areaToday.date
            else:
                dates_range_start = datetime.datetime.now().date()
                dates_range_end = datetime.datetime.now().date()

        if dates_range_start and dates_range_end:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area, date__range=(dates_range_start, dates_range_end))

        for a in area_per_day_list:
            dates.append(a.date.strftime("%d.%m"))

            temp = int(a.today_share_counter.split(',')[0])
            todayVK.append(temp)
            if temp > statistic['vk']:
                statistic['vk'] = temp

            temp = int(a.today_share_counter.split(',')[1])
            todayFB.append(temp)
            if temp > statistic['fb']:
                statistic['fb'] = temp

            temp = int(a.today_share_counter.split(',')[2])
            todayTW.append(temp)
            if temp > statistic['tw']:
                statistic['tw'] = temp

            temp = int(a.today_share_counter.split(',')[3])
            todayOD.append(temp)
            if temp > statistic['od']:
                statistic['od'] = temp

            temp = int(a.today_share_counter.split(',')[4])
            todayGP.append(temp)
            if temp > statistic['gp']:
                statistic['gp'] = temp

            temp = int(a.today_share_counter.split(',')[5])
            todayMA.append(temp)
            if temp > statistic['ma']:
                statistic['ma'] = temp

            temp = int(a.today_share_counter.split(',')[6])
            todayLI.append(temp)
            if temp > statistic['li']:
                statistic['li'] = temp

            temp = int(a.today_share_counter.split(',')[7])
            todayLJ.append(temp)
            if temp > statistic['lj']:
                statistic['lj'] = temp

        statistic['all'] = statistic['vk'] + statistic['fb'] + statistic['tw'] + statistic['od'] + statistic['gp'] + statistic['ma'] + statistic['li'] + statistic['lj']

        return render(request, template_name,
        {
            'statistic': statistic,
            'dates_range_start': dates_range_start.strftime("%d.%m.%Y"),
            'dates_range_end': dates_range_end.strftime("%d.%m.%Y"),
            'page': { 'title': title, 'header': header },
            'dates': dates,
            'todayVK': todayVK,
            'todayFB': todayFB,
            'todayTW': todayTW,
            'todayOD': todayOD,
            'todayGP': todayGP,
            'todayMA': todayMA,
            'todayLI': todayLI,
            'todayLJ': todayLJ,
            'list_page_detail': list_page_detail
        })
    else:
        return HttpResponseRedirect('/webmaster-area/detail-error/')

@login_required
def delete(request, pk):
    profile_user = None

    if request.user.is_staff and request.session.get('profile', False):
        profile_user = User.objects.get(pk=request.session.get('profile').get('pk'))

    try:
        if profile_user:
            WebmasterAreaModel.objects.get(pk=pk, buttons_constructor__cabinet_webmaster__user=profile_user).delete()

            return HttpResponseRedirect('/admin/profile/'+str(profile_user.pk)+'/?next=/webmaster-area/')
        else:
            WebmasterAreaModel.objects.get(pk=pk, buttons_constructor__cabinet_webmaster__user=request.user).delete()
    except:
        pass

    return HttpResponseRedirect('/webmaster-area/')

@login_required
def update(request, pk):
    request_instance = None
    profile_user = None

    if request.user.is_staff and request.session.get('profile', False):
        profile_user = User.objects.get(pk=request.session.get('profile').get('pk'))

    try:
        request_instance = WebmasterAreaModel.objects.get(pk=pk, buttons_constructor__cabinet_webmaster__user=profile_user) if profile_user is not None else WebmasterAreaModel.objects.get(pk=pk, buttons_constructor__cabinet_webmaster__user=request.user)
    except:
        pass

    if request_instance and request.method == 'POST':

        area_category_list = request.POST.getlist('area_category','')
        area_category_clear = ''

        for a in area_category_list:
            area_category_clear += AreaCategory.objects.get(pk=a).name + ','
        area_category_clear = area_category_clear[:-1]

        request_post_data = {
            'name_area': request_instance.name_area,
            'url': request_instance.url,
            #TODO: disable change name_area and url else need to check for conflict name_area and url
            #'name_area': request.POST.get('name_area', ''),
            #'url': request.POST.get('url', ''),
            'ad_type': request.POST.get('ad_type', ''),
            'area_category': area_category_clear
        }
        webmaster_area_form = WebmasterAreaForm(data=request_post_data, instance=request_instance, auto_id=False)

        if webmaster_area_form.is_valid():

            webmaster_area = webmaster_area_form.save(commit=False)
            webmaster_area.save()

            if profile_user:
                return HttpResponseRedirect('/admin/profile/'+str(profile_user.pk)+'/?next=/webmaster-area/')

    return HttpResponseRedirect('/webmaster-area/')

@login_required
def create(request):

    if request.method == 'POST':
        profile_user = None

        if request.user.is_staff and request.session.get('profile', False):
            profile_user = User.objects.get(pk=request.session.get('profile').get('pk'))

        area_category_list = request.POST.getlist('area_category','')
        area_category_clear = ''
        for a in area_category_list:
            area_category_clear += AreaCategory.objects.get(pk=a).name + ','
        area_category_clear = area_category_clear[:-1]
        request_post_data = {
            'name_area': request.POST.get('name_area', ''),
            'url': request.POST.get('url', ''),
            'ad_type': request.POST.get('ad_type', ''),
            'area_category': area_category_clear
        }
        webmaster_area_form = WebmasterAreaForm(data=request_post_data, auto_id=False)

        #user_wma_list = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user)
        all_wma_list = WebmasterAreaModel.objects.select_related("buttons_constructor__cabinet_webmaster__user").all()
        user_wma_names_list = []
        all_wma_urls_list = []

        #for area in user_wma_list:
        #    user_wma_names_list.append(area.name_area)
        for area in all_wma_list:
            if area.buttons_constructor.cabinet_webmaster.user == profile_user if profile_user is not None else request.user:
                user_wma_names_list.append(area.name_area)
            all_wma_urls_list.append(area.url)

        isNameAreaAlreadyExist = request_post_data.get('name_area','') in user_wma_names_list
        isUrlAreaAlreadyExist = urlparse(request_post_data.get('url','')).netloc in all_wma_urls_list

        if webmaster_area_form.is_valid() and isNameAreaAlreadyExist == False and isUrlAreaAlreadyExist == False:

            webmaster_area = webmaster_area_form.save()
            #webmaster_area.buttons_constructor = request.user.cabinet_webmaster.buttons_constructor.all()[0]
            try:
                webmaster_area.buttons_constructor = ButtonsConstructorModel.objects.filter(cabinet_webmaster=profile_user.cabinet_webmaster).order_by('-pk')[0] if profile_user is not None else ButtonsConstructorModel.objects.filter(cabinet_webmaster=request.user.cabinet_webmaster).order_by('-pk')[0]
            except Exception as instance:
                webmaster_area.buttons_constructor = ButtonsConstructorModel.objects.create(cabinet_webmaster=profile_user.cabinet_webmaster, btns_images=BtnsImages.objects.latest('pk')) if profile_user is not None else ButtonsConstructorModel.objects.create(cabinet_webmaster=request.user.cabinet_webmaster, btns_images=BtnsImages.objects.latest('pk'))

            webmaster_area.save()

            if profile_user:
                return HttpResponseRedirect('/admin/profile/'+str(profile_user.pk)+'/?next=/webmaster-area/')

    return HttpResponseRedirect('/webmaster-area/')

def setcounterprivate(url):
    snc = ''
    val = URLValidator()

    try:
        val(url)
    except:
        return '-1'

    if url:
        share_count_methods = [
            {'http://vk.com/share.php?act=count&url='+url: 'count\([0-9]+, ([0-9]+)\)'},
            {'https://api.facebook.com/method/fql.query?format=json&query=SELECT%20share_count%20FROM%20link_stat%20WHERE%20url=%27'+url+'%27': 'share_count":([0-9])+'},
            {'tw': 'twitter'},
            {'https://connect.ok.ru/dk?st.cmd=extLike&ref='+url: 'ODKL.updateCount\(.*,\'([0-9])+\''},
            {'http://free.sharedcount.com/url?url='+url+'&apikey=e02e2352f161d72d0466e71ee4fc812dfe321e32': '"GooglePlusOne":([0-9]+)'},
            {'http://connect.mail.ru/share_count?url_list='+url: '"shares":([0-9]+)'},
            {'https://www.linkedin.com/countserv/count/share?url='+url: '"count":([0-9]+)'},
            {'lj': 'lj'}
        ]

        for d in share_count_methods:
            for u,m in d.items():
                try:
                    val(u)
                except:
                    snc += '0,'
                else:
                    try:
                        timeout = 4.0

                        response = requests.get(u, timeout=timeout)
                        re_result = re.findall(m, response.text)
                        
                        if len(re_result) > 0:
                            snc += re_result[0] + ','
                        else:
                            snc += '0,'
                    except requests.Timeout as err:
                        #return HttpResponse(err)
                        return '-1'
                    except:
                        return '-1'

        snc = snc[:-1]
        return snc

    return '-1'

def getAdvert(request, cook):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc

    wma_object = WebmasterAreaModel.objects.select_related('buttons_constructor').filter(url=parsed_referer).last()

    if wma_object:
        answer = {}

        #TODO: create new areaToday
        '''
        try:
            wma_today = AreaToday.objects.get(webmaster_area=wma_object, date=datetime.date.today())
        except:
            wma_today = AreaToday.objects.create(webmaster_area=wma_object, date=datetime.date.today())
        '''

        try:
            advert = Advert.objects.get(buttons_constructor__pk = wma_object.buttons_constructor.pk)
        except:
            advert = None

        if advert:

            if len(advert.get_ad_allow_display().split('x')) > 1:

                banner_w = advert.get_ad_allow_display().split('x')[0]
                banner_h = advert.get_ad_allow_display().split('x')[1]

                try:
                    area_today = AreaToday.objects.filter(webmaster_area=wma_object).last()
                except:
                    area_today = None

                request_ip = request.META.get('REMOTE_ADDR', '')
                request_userAgent = request.META.get('HTTP_USER_AGENT', '')
                request_advCook = cook

                pool = urllib3.PoolManager()

                url = 'myclk.net/rtb/bid?partner=sharewall'
                data = '{"cur": ["RUB"], \
                    "device":{\
                        "ip": "%s", "ua": "%s" \
                    },\
                    "id": "1453290563728",\
                    "tmax": 120,\
                    "imp": [{\
                        "id": "1",\
                        "banner": {\
                            "h": %d,\
                            "pos": 0,\
                            "w": %d\
                        },\
                        "bidfloor": 0,\
                        "bidfloorcur": "RUB"\
                    }],\
                    "site": {\
                        "id": "%s",\
                        "page": "%s",\
                        "ref": ""\
                    },\
                    "user":{\
                        "id": "%s"\
                    }\
                }'%(request_ip, request_userAgent, int(banner_h), int(banner_w), wma_object.pk, request_referer, request_advCook)#.format(ip=request_ip, agent=request_userAgent)

                r = pool.urlopen(
                    'POST', 
                    url, 
                    headers={'Content-Type': 'application/json'},
                    body=data
                )

                advert_response = r.data.decode('utf-8')
                #return HttpResponse('sharewallAdvResponse('+advert_response+');')
                try:
                    #raise error if bad request
                    advert_json = json.loads(advert_response)
                    #return HttpResponse('sharewallAdvResponse('+advert_json+');')
                    advert_json_adm = advert_json['seatbid'][0]['bid'][0]['adm']
                    advert_json_price = advert_json['seatbid'][0]['bid'][0]['price']
                    advert_json_nurl = advert_json['seatbid'][0]['bid'][0]['nurl']
                except:
                    return HttpResponse('console.log("no bid");')

                pattern_auc_price = '${AUCTION_PRICE}'
                index_price = advert_json_nurl.index(pattern_auc_price)

                nurl_url = advert_json_nurl[:index_price] + str(advert_json_price)

                r = pool.urlopen('GET', nurl_url)

                if area_today:
                    area_today.today_show_counter += 1
                    area_today.today_money += float(advert_json_price / 1000)
                    area_today.save()

                    try:
                        cabinet = advert.cabinet_webmaster
                        cabinet.money += float(advert_json_price / 1000)
                        cabinet.save()
                    except:
                        return HttpResponse('bad cabinet')

                answer = {
                    'adm': advert_json_adm,
                    #'nurl_response': r.data.decode('utf-8'),
                    #'nurl_url': nurl_url,
                    #'request_ip': request_ip,
                    #'useragent': request_userAgent,
                    #'area_pk': wma_object.pk,
                    #'request_page': request_referer,
                    #'request_advCook': request_advCook,
                    #'data': data,
                    #'advert': advert_response,
                    #'advert_json': advert_json,
                    #'advert_json_adm': advert_json['seatbid'][0]['bid'][0]['adm'],
                    #'advert_json_price': advert_json_price,
                    #'advert_json_nurl': advert_json['seatbid'][0]['bid'][0]['nurl'],
                    }

                return HttpResponse('sharewallAdvResponse('+json.dumps(answer)+');')

    return HttpResponse('bad id')
    #return JsonResponse({ })

def checkconfig(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc

    wma_object = WebmasterAreaModel.objects.select_related('buttons_constructor').filter(url=parsed_referer).last()

    if wma_object:
        answer = ''
        history_referrer = request.GET.get('referrer', 'none referrer')
        history_rr = request.GET.get('rr', 'none rr')
        request_url = request.GET.get('url', 'none url')

        #TODO: to lower case
        request_url = request_url.lower()

        request_title = request.GET.get('title', 'none title')
        snc = request.GET.get('snc', 'none snc')
        snc = snc[:-1]
        history_parsed_referrer = urlparse(history_referrer).netloc
        list_sn = SocialNetworks.objects.all()
        list_parsed_sn = [urlparse(sn.url).netloc for sn in list_sn]
        index_sn = None
        answer += 'console.log("history_parsed_referrer = %s");'%history_parsed_referrer
        if history_referrer != history_rr and history_parsed_referrer in list_parsed_sn:
            index_sn = list_parsed_sn.index(history_parsed_referrer)
            answer += 'console.log("list_parsed = {0} history_parsed_referrer = {1} index = {2} history_rr = {3} history_referrer = {4}");'.format(list_parsed_sn, history_parsed_referrer, index_sn, history_rr, history_referrer)

        #Page detail
        #Disable page_today
        #Total counters in page_detail now work like today counters! They do not collect digits for all time, but update every time then call
        request_url_html = urllib.request.urlopen(request_url)
        soup = BeautifulSoup(request_url_html)

        if parsed_referer == urlparse(request_url).netloc and request_url_html.status == 200:
            answer += 'console.log("url ok");'
            answer += 'console.log("snc from client: '+snc+'");'

            snc_server = setcounterprivate(request_url)
            if not snc_server == '-1':
                answer += 'console.log("snc from server: '+snc_server+'");'
                snc = snc_server
            
            #wma today!
            try:
                wma_today = AreaToday.objects.get(webmaster_area=wma_object, date=datetime.date.today())
            except:
                wma_today = AreaToday.objects.create(webmaster_area=wma_object, date=datetime.date.today()) #,today_share_counter=snc)

            list_sn_shortcuts = [sn.shortcut for sn in list_sn]
            #fix tw, lj
            if request.GET.get("sn", False):
                index_fix_share = list_sn_shortcuts.index(request.GET.get("sn"))
                temp_share_counter = [int(s) for s in snc.split(',')]
                temp_share_counter[index_fix_share] += 1
                snc = ''
                for i in temp_share_counter:
                    snc += str(i) + ','
                snc = snc[:-1]
                answer += 'console.log("snc fix: '+snc+'");'

            try:
                page_detail = PageDetail.objects.get(webmaster_area=wma_object, url=request_url)
                
                if page_detail:
                    page_detail.title = soup.title.string
                    page_detail.total_share_counter = snc

                    if index_sn is not None:
                        short_sn = list_sn[index_sn].shortcut
                        index_sn = list_sn_shortcuts.index(short_sn)
                        temp_social_counter = [int(s) for s in page_detail.total_social_counter.split(',')]
                        temp_social_counter[index_sn] += 1
                        page_detail.total_social_counter = ''
                        for i in temp_social_counter:
                            page_detail.total_social_counter += str(i) + ','
                        page_detail.total_social_counter = page_detail.total_social_counter[:-1]

                    page_detail.save()
                    answer += 'console.log("'+str(page_detail) + ' updated!");' 
            except:
                page_detail = PageDetail.objects.create(webmaster_area=wma_object, total_share_counter=snc, url=request_url, title=soup.title.string)

                if page_detail:
                    if index_sn is not None:
                        short_sn = list_sn[index_sn].shortcut
                        index_sn = list_sn_shortcuts.index(short_sn)
                        temp_social_counter = [int(s) for s in page_detail.total_social_counter.split(',')]
                        temp_social_counter[index_sn] += 1
                        page_detail.total_social_counter = ''
                        for i in temp_social_counter:
                            page_detail.total_social_counter += str(i) + ','
                        page_detail.total_social_counter = page_detail.total_social_counter[:-1]
                        page_detail.save()

                    answer += 'console.log("'+str(page_detail) + ' created!");' 
        else:
            answer = "bad id!"
            return HttpResponse(answer)

        answer += '    document.cookie = "_sharewallrr=; expires=Thu, 01 Jan 1970 00:00:00 UTC";'
        answer += '    var date = new Date(); date.setTime(date.getTime() + 24*60*60*1000);'
        answer += '    document.cookie = "_sharewallrr=%s'%history_referrer+'; path=%s'%urlparse(request_url).path+'; max-age="+24*60*60+"; expires="+date.toGMTString();'
    else:
        answer = 'bad id!'
    return HttpResponse(answer)


def setcounter(request):
    url = request.GET.get("url")
    snc_server = setcounterprivate(url)

    return HttpResponse(snc_server)


def getconfig(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc

    wma_object = WebmasterAreaModel.objects.select_related('buttons_constructor').filter(url=parsed_referer).last()
    if wma_object:

        list_sn = SocialNetworks.objects.all()

        SOCIAL_DEFAULT = ''
        list_sn_unic = {}

        for s in list_sn:
            if not s.shortcut in SOCIAL_DEFAULT:
                SOCIAL_DEFAULT += s.shortcut + ','
                list_sn_unic[s.shortcut] = s

        SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]

        #buttons_constructor
        btncr = wma_object.buttons_constructor

        if btncr.form_buttons=="SQ":
            sprite = btncr.btns_images.path.replace("/ci/", "/sq/")
        else:
            sprite = btncr.btns_images.path

        sprite = sprite.replace("/BIG/", "/"+btncr.size_buttons+"/")

        #Advert
        try:
            advert = Advert.objects.get(buttons_constructor=btncr)
        except:
            advert = None

        if btncr.size_buttons == 'BIG':
            btn_width = '41'
            btn_height = btn_width
            btn_margin = '15'
            btn_logo_pos = '-328'
            btn_counter_style = 'height:41px; width:64px; font: 400 14px / 41px Roboto;'
            if advert:
                btn_adv_pos = advert.btn_image.bg_position
        elif btncr.size_buttons == 'MED':
            btn_width = '31'
            btn_height = btn_width
            btn_margin = '5'
            btn_logo_pos = '-248'
            btn_counter_style = 'height:31px; width:48px; font: 400 12.5px / 31px Roboto; background-size:cover;'
            if advert:
                btn_adv_pos = advert.btn_image.bg_position_med
        else:
            btn_width = '21'
            btn_height = btn_width
            btn_margin = '0'
            btn_logo_pos = '-168'
            btn_counter_style = 'height:21px; width:31px; font: 400 10.5px / 21px Roboto; background-size:cover;'
            if advert:
                btn_adv_pos = advert.btn_image.bg_position_sml

        answer = 'function sharewallWrapper(){'
        answer += '(function sharewallConstruct($, d, w) {'

        answer += '    $("div#sharewallContainer").html(\'\');'

        if btncr.with_background:
            answer += '$("div#sharewallContainer").css({"background-color": "'+btncr.background_color+'", "padding-top": "6px", "border-radius": "10px", "display": "inline-block"});'

        if btncr.location_buttons == "VE":
            answer += '$("div#sharewallContainer").css("float","left");'

        #Adv
        if advert:
            answer += 'w.sharewallAdvResponse = function(r){\
                        console.log(r);\
                        if($("#sharewallAdvertContainer").length > 0){\
                        $("div#sharewallAdvertContainer").html(r.adm).show();\
                        }else{\
                        $("div#sharewallContainer").after("<div id=\'sharewallAdvertContainer\'></div>").next("#sharewallAdvertContainer").html(r.adm).show();\
                        }\
                      };'

            answer += 'var advCook = d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallAdvrr\s*\=\s*([^;]*).*$)|^.*$/, "$1");\
                        if(advCook == ""){\
                            var date_expires = new Date(new Date().setFullYear(new Date().getFullYear()+1));'
            answer += 'advCook = "{0}";'.format(uuid.uuid4())
            answer += 'document.cookie = "_sharewallAdvrr="+advCook+"; path=/; expires="+date_expires.toGMTString();\
                        }'
                       
            answer += '$("body").append(\'<img src="http://sync.mecash.ru/uid/match?partner=sharewall&id=\'+advCook+\'" style="width: 1px; height: 1px; opacity: 0; position: absolute;" />\');'

            if advert.ad_type == 'BUY':
                answer += '$("div#sharewallContainer").append(\'<span id="sAdvBtn" style="width:'+btn_width+'px; height:'+btn_height+'px; margin-right:'+btn_margin+'px; display:inline-block; background-image: url(http://sharewall.ru/static/sharewall-template/'+sprite+'); background-repeat: no-repeat; '+btn_adv_pos+' cursor: pointer;"></span>\''

                if btncr.location_buttons == "VE":
                    answer += '+\'<br/>\''
                answer += ');'
                answer += '$("div#sharewallContainer > #sAdvBtn").click(function(){\
                            console.log("advert click");\
                            $.ajax({ url: "http://sharewall.ru/webmaster-area/getadvert/"+advCook, type: "POST", dataType: "jsonp" });\
                           });'
            else:
                answer += 'w.setTimeout(function(){\
                            console.log("advert setTimeout=3000");\
                            $.ajax({ url: "http://sharewall.ru/webmaster-area/getadvert/"+advCook, type: "POST", dataType: "jsonp" });\
                           },3000);'

        for sn in btncr.social_networks.split(','):
            answer += 'var new_href = "";'
            if sn == 'vk':
                answer += 'new_href = "http://vk.com/share.php?url="+{0}+{1}+{2}+{3};'.format(
                        'encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else 'encodeURIComponent(d.URL)',
                    '"&description="+encodeURIComponent("'+btncr.page_description+'")' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&description="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&title="+encodeURIComponent("'+btncr.page_title+'")' if btncr.page_title else '"&title="+encodeURIComponent(d.title)',
                    '"&noparse=true"'
                )
            if sn == "fb":
                answer += 'new_href = "https://www.facebook.com/sharer/sharer.php?s=100"+{0}+{1}+{2};'.format(
                        '"&p[url]="+encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else '"&p[url]="+encodeURIComponent(d.URL)',
                    '"&p[summary]="+encodeURIComponent("'+btncr.page_description+'")' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&p[summary]="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&p[title]="+encodeURIComponent("'+btncr.page_title+'")' if btncr.page_title else '"&p[title]="+encodeURIComponent(d.title)'
                )
            if sn == "tw":
                answer += 'new_href = "https://www.twitter.com/share?"+{0}+{1};'.format(
                        '"url="+encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else '"url="+encodeURIComponent(d.URL)',
                    '"&text="+encodeURIComponent("'+btncr.page_title+'")' if btncr.page_title else '"&text="+encodeURIComponent(d.title)'
                )
            if sn == "od":
                answer += 'new_href = "http://www.odnoklassniki.ru/dk?st.cmd=addShare&st.s=1"+{0}+{1};'.format(
                        '"&st._surl="+encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else '"&st._surl="+encodeURIComponent(d.URL)',
                    '"&st.comments="+encodeURIComponent("'+btncr.page_description+'")' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&st.comments="+encodeURIComponent(d.head.children.Description.content) : "")'
                )
            if sn == "gp":
                answer += 'new_href = "https://plus.google.com/share?"+{0};'.format(
                        '"url="+encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else '"url="+encodeURIComponent(d.URL)'
                )
            if sn == "ma":
                answer += 'new_href = "http://connect.mail.ru/share?"+{0}+{1}+{2};'.format(
                        '"url="+encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else '"url="+encodeURIComponent(d.URL)',
                    '"&description="+encodeURIComponent("'+btncr.page_description+'")' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&description="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&title="+encodeURIComponent("'+btncr.page_title+'")' if btncr.page_title else '"&title="+encodeURIComponent(d.title)'
                )
            if sn == "li":
                answer += 'new_href = "http://www.linkedin.com/shareArticle?mini=true"+{0}+{1}+{2};'.format(
                        '"&url="+encodeURIComponent("'+btncr.page_url+'")' if btncr.page_url else '"&url="+encodeURIComponent(d.URL)',
                    '"&summary="+encodeURIComponent("'+btncr.page_description+'")' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&summary="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&title="+encodeURIComponent("'+btncr.page_title+'")' if btncr.page_title else '"&title="+encodeURIComponent(d.title)'
                )
            if sn == "lj":
                answer += 'new_href = "http://www.livejournal.com/update.bml?"+{0}+{1};'.format(
                    '"event="+encodeURIComponent("'+btncr.page_description+'")' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "event="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&subject="+encodeURIComponent("'+btncr.page_title+'")' if btncr.page_title else '"&subject="+encodeURIComponent(d.title)'
                )

            if btncr.size_buttons == 'BIG':
                temp_size = list_sn_unic[sn].img_bd_pos
            elif btncr.size_buttons == 'MED':
                temp_size = list_sn_unic[sn].img_bd_pos_med
            else:
                temp_size = list_sn_unic[sn].img_bd_pos_sml

            answer += '$("div#sharewallContainer").append(\'\''
            answer += '   +\'<a data-share-sn="{0}" href=\'+new_href+\' style="width:{1}px; height:{2}px; margin-right:{3}px; display:inline-block; background-image: url(http://sharewall.ru/static/sharewall-template/{4}); background-repeat: no-repeat; {5}"></a>\''.format(sn, btn_width, btn_height, btn_margin, sprite, temp_size)
            if btncr.location_buttons == "VE":
                answer += '+\'<br>\''
            answer += ');'

        answer += '$("div#sharewallContainer").append(\'<a target="_blank" href="//sharewall.ru" style="width:'+btn_width+'px; height:'+btn_width+'px; margin-right:'+btn_margin+'px; display:inline-block; background-image: url(http://sharewall.ru/static/sharewall-template/'+sprite+'); background-repeat: no-repeat; background-position: '+btn_logo_pos+'px 0px;"></a>\');'
        if btncr.with_counter:
            if btncr.location_buttons == "VE":
                answer += '$("div#sharewallContainer").append("<br/>");'
            answer += '$("div#sharewallContainer").append(\'<span id="shareCounter" style="margin-left:3px; display:inline-block; color:#fff; text-align:center; vertical-align: top; background-image: url(http://sharewall.ru/static/sharewall-template/images/btns-counter-black.png); background-repeat: no-repeat; cursor: default; '+btn_counter_style+'">0</span>\');'

        answer += '    $("body").append("<div id=\'sharewallSNC\' style=\'display: none\'></div>");'
        for s in SOCIAL_DEFAULT.split(","):
            answer += '$("body div#sharewallSNC").append("<span data-share-sn-id=\'%s\' data-share-sn-count=\'0\' style=\'display: none;\'></span>");'%s
        answer += '    function sharewallSetSNC(sn, counter="0"){\
                           $sn = $("body div#sharewallSNC").find("span[data-share-sn-id="+sn+"]");\
                           counterSn = counter;\
                           console.log(sn+": "+counterSn+" counterSn");\
                           counter = parseInt(counter) - parseInt($sn.attr("data-share-sn-count"));\
                           console.log(sn+": "+counter+" counter");\
                           $sn.attr("data-share-sn-count", counterSn);\
                           $buttonCounter = $("div#sharewallContainer").find("span#shareCounter");\
                           currentCounter = $buttonCounter.text();\
                           updatedCounter = parseInt(counter)+ parseInt(currentCounter);\
                           $buttonCounter.text(updatedCounter);\
                       }'
        answer += '    w.VK = { Share: { count: function(index, counter){\
                           sharewallSetSNC("vk", counter);\
                       }}};'
        answer += '    w.ODKL = { updateCount: function(index, count){ sharewallSetSNC("od", count); }                       };'
        answer += '    w.sharewallMyMailCallback = function(response){ sharewallSetSNC("ma", response[d.URL]["shares"]);\
                       };'
        answer += '    function sharewallGetAllSNC(){\
                           var snc = "";\
                           $("body div#sharewallSNC").find("span").each(function(i, e){ snc += $(e).attr("data-share-sn-count")+","; });\
                           console.log("sharewallGetAllSNC: "+snc);\
                           return snc;\
                       }'
        answer += '$.sharewallSharedCount = function(url, fn) {\
                       url = encodeURIComponent(url || location.href);\
                       var domain = "//free.sharedcount.com";\
                       var ak = "e02e2352f161d72d0466e71ee4fc812dfe321e32";\
                       var arg = {\
                           data: {\
                               url: url,\
                               apikey: ak\
                           },\
                           url: domain + "/url",\
                           cache: true,\
                           dataType: "json"\
                       };\
                       if ("withCredentials" in new XMLHttpRequest) {\
                           arg.success = fn;\
                       } else {\
                           var cb = "sc_" + url.replace(/\W/g, "");\
                           window[cb] = fn;\
                           arg.jsonpCallback = cb;\
                           arg.dataType += "p";\
                       }\
                       return $.ajax(arg);\
                   };'
        answer += '$.sharewallSharedCount(location.href, function(data){\
                       if(data.GooglePlusOne){\
                           sharewallSetSNC("gp", data.GooglePlusOne);\
                       }\
                   });'
        answer += '    $.when(\
                           $.ajax({ url: "http://vk.com/share.php?act=count&url="+encodeURIComponent(d.URL), dataType: "jsonp" }),\
                           $.ajax({ url: "https://api.facebook.com/method/fql.query?format=json&query=SELECT%20share_count%20FROM%20link_stat%20WHERE%20url=" + "\'" +encodeURIComponent(d.URL)+ "\'", dataType: "jsonp", success: function(data, status, jqXHR) {\
                           if(status == "success" && data[0]) {\
                               if(data[0].share_count > 0) {\
                                   sharewallSetSNC("fb", data[0].share_count);\
                               }\
                           }\
                           }}),\
                           $.ajax({ url: "https://connect.ok.ru/dk?st.cmd=extLike&ref="+encodeURIComponent(d.URL), dataType: "jsonp", jsonp: false }),\
                           $.ajax({ url: "http://connect.mail.ru/share_count?url_list="+encodeURIComponent(d.URL)+"&callback=1&func=sharewallMyMailCallback", dataType: "jsonp", jsonp: false }),\
                           $.ajax({ url: "https://www.linkedin.com/countserv/count/share?url=" + encodeURIComponent(d.URL), dataType: "jsonp", success: function(response) { sharewallSetSNC("li", response.count); }\
                           })\
                       ).done(w.setTimeout(function(){\
                       console.log("done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));'

        answer += ' $("div#sharewallContainer").children().each(\
            function(i,e){\
                $this = $(e);\
                if($this.is("a[data-share-sn]")){\
                    $this.click(\
                        function() {\
                            $this = $(this); \
                            sn = $this.data("shareSn");\
                            var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;\
                            var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;\
                            var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;\
                            var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;\
                            var left = ((width / 2) - (626 / 2)) + dualScreenLeft;\
                            var top = ((height / 2) - (436 / 2)) + dualScreenTop;\
                            new_window = w.open($this.attr("href"), "", "left="+left+",top="+top+",personalbar=0,scrollbars=1,resizable=1,toolbar=0,width=626,height=436"); \
                            var popup_w_interval = w.setInterval(function() {'
        answer += '             console.log("popup opened..."+sn);\
                                if (new_window.closed !== false) {\
                                    w.clearInterval(popup_w_interval);\
                                    console.log("popup closed! "+sn);'
        #TODO: counter each sn
        answer += 'if(sn=="lj"){\
                       sharewallSetSNC("lj", 1);\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, sn: "lj", rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                   }'
        answer += 'if(sn=="tw"){\
                       sharewallSetSNC("tw", 1);\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, sn: "tw", rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                   }'
        answer += 'if(sn=="vk"){\
                       $.when($.ajax({ url: "http://vk.com/share.php?act=count&url="+encodeURIComponent(d.URL), dataType: "jsonp" })\
                       ).done(w.setTimeout(function(){\
                       console.log("VK done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));\
                   }'
        answer += 'if(sn=="fb"){\
                       $.when($.ajax({ url: "https://api.facebook.com/method/fql.query?format=json&query=SELECT%20share_count%20FROM%20link_stat%20WHERE%20url=" + "\'" +encodeURIComponent(d.URL)+ "\'", dataType: "jsonp", success: function(data, status, jqXHR) {\
                        if(status == "success" && data[0]) {\
                             if(data[0].share_count > 0) {\
                                 sharewallSetSNC("fb", data[0].share_count);\
                             }\
                        }\
                        }})\
                       ).done(w.setTimeout(function(){\
                       console.log("FB done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));\
                    }'
        answer += 'if(sn=="od"){\
                       $.when($.ajax({ url: "https://connect.ok.ru/dk?st.cmd=extLike&ref="+encodeURIComponent(d.URL), dataType: "jsonp", jsonp: false })\
                       ).done(w.setTimeout(function(){\
                       console.log("OD done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));\
                    }'
        answer += 'if(sn=="ma"){\
                       $.when($.ajax({ url: "http://connect.mail.ru/share_count?url_list="+encodeURIComponent(d.URL)+"&callback=1&func=sharewallMyMailCallback", dataType: "jsonp", jsonp: false })\
                       ).done(w.setTimeout(function(){\
                       console.log("MA done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));\
                    }'
        answer += 'if(sn=="gp"){\
                       $.sharewallSharedCount(location.href, function(data){\
                           if(data.GooglePlusOne){\
                               sharewallSetSNC("gp", data.GooglePlusOne);\
                           }\
                           w.setTimeout($.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } })\
                       ,1000);\
                       console.log("GP done setTimeout=1000");\
                       });\
                   }'
        answer += 'if(sn=="li"){\
                       $.when($.ajax({ url: "https://www.linkedin.com/countserv/count/share?url=" + encodeURIComponent(d.URL), dataType: "jsonp", success: function(response) { sharewallSetSNC("li", response.count); }\
                        })\
                       ).then(w.setTimeout(function(){\
                       console.log("LI done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));\
                   }'

        answer += '}\
                }, 900);\
                        return false; }\
                    ); \
                }}\
                );\
        })(window.jQuery, document, window)'
        answer += '}'
        answer += 'if(window.jQuery){\
                       sharewallWrapper();\
                   }else{\
                       var headTag = document.getElementsByTagName("head")[0];\
                       var jqTag = document.createElement("script");\
                       jqTag.type = "application/javascript";\
                       jqTag.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js";\
                       jqTag.onload = sharewallWrapper;\
                       headTag.appendChild(jqTag);\
                   }'

    else:
        answer = 'console.log("bad id!")' 
    return HttpResponse(answer, content_type='application/javascript')
