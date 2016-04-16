import datetime, json, os
import re
import sys
from urllib.parse import urlparse
import urllib.request
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from webmaster_area.models import WebmasterAreaModel, PageDetail, AreaToday
from buttons_constructor.models import SocialNetworks, BtnsImages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from webmaster_area.forms import WebmasterAreaForm, AreaCategory
from buttons_constructor.models import ButtonsConstructorModel, BtnsImages
from bs4 import BeautifulSoup

class WebmasterAreaIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'webmaster_area/index.html'
    title = 'Webmaster area'
    header = 'Площадки'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name,
        {
            "areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
            "page": { "title": self.title, 'header': self.header },
            "ad_type": "Нормальный,Для взрослых",
            "area_category": AreaCategory.objects.all()
        })

@login_required
def statistic(request):
    template_name = 'webmaster_area/statistic.html'
    title = 'Статистика'
    header = 'Статистика'

    return render(request, template_name,
    {
        'areas': WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),
        'page': { 'title': title, 'header': header }
    })

@login_required
def detailmain(request):
    template_name = 'webmaster_area/detail-main.html'
    
    dates = []
    shows = []
    shares = []
    socials = []
    clicks = []
    money = []
    dates_range_start = None
    dates_range_end = None
    isEmpty = True

    areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user)
    
    if areas.first():
        isEmpty = False

    try:
        request_dateRange = request.GET.get('daterange').split(' - ')
        dates_range_start = datetime.datetime.strptime(request_dateRange[0], "%d.%m.%Y").date()
        dates_range_end = datetime.datetime.strptime(request_dateRange[1], "%d.%m.%Y").date()
    except Exception as inst:
        temp_areaTodayList = None
        if not isEmpty:
            temp_areaTodayList = AreaToday.objects.filter(webmaster_area=areas.first())

        if temp_areaTodayList is not None and temp_areaTodayList.first():
            temp_areaToday = temp_areaTodayList.first()
            dates_range_start = temp_areaToday.date#.strftime("%d.%m.%Y")
            temp_areaToday = temp_areaTodayList.last()
            dates_range_end = temp_areaToday.date#.strftime("%d.%m.%Y")
        else:
            dates_range_start = datetime.datetime.now().date()
            dates_range_end = datetime.datetime.now().date()

    for area in areas:

        if dates_range_start and dates_range_end:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area, date__range=(dates_range_start, dates_range_end))#["2016-04-11", "2016-04-12"])
        else:
            area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        #!
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

                last_day.today_share_counter = last_day.today_share_counter[:-1]

                last_day.save()

        for a in area_per_day_list:
            temp_areaPDay_date = a.date.strftime("%d.%m")

            if temp_areaPDay_date in dates:
                shares[dates.index(temp_areaPDay_date)]+=(
                    int(a.today_share_counter.split(',')[0])+
                    int(a.today_share_counter.split(',')[1])+
                    int(a.today_share_counter.split(',')[2])+
                    int(a.today_share_counter.split(',')[3])+
                    int(a.today_share_counter.split(',')[4])+
                    int(a.today_share_counter.split(',')[5])+
                    int(a.today_share_counter.split(',')[6])+
                    int(a.today_share_counter.split(',')[7])
                )
                socials[dates.index(temp_areaPDay_date)]+=(
                    int(a.today_social_counter.split(',')[0])+
                    int(a.today_social_counter.split(',')[1])+
                    int(a.today_social_counter.split(',')[2])+
                    int(a.today_social_counter.split(',')[3])+
                    int(a.today_social_counter.split(',')[4])+
                    int(a.today_social_counter.split(',')[5])+
                    int(a.today_social_counter.split(',')[6])+
                    int(a.today_social_counter.split(',')[7])
                )
            else:
                dates.append(temp_areaPDay_date)
                shares.append(
                        int(a.today_share_counter.split(',')[0])+
                        int(a.today_share_counter.split(',')[1])+
                        int(a.today_share_counter.split(',')[2])+
                        int(a.today_share_counter.split(',')[3])+
                        int(a.today_share_counter.split(',')[4])+
                        int(a.today_share_counter.split(',')[5])+
                        int(a.today_share_counter.split(',')[6])+
                        int(a.today_share_counter.split(',')[7])
                        )
                socials.append(
                        int(a.today_social_counter.split(',')[0])+
                        int(a.today_social_counter.split(',')[1])+
                        int(a.today_social_counter.split(',')[2])+
                        int(a.today_social_counter.split(',')[3])+
                        int(a.today_social_counter.split(',')[4])+
                        int(a.today_social_counter.split(',')[5])+
                        int(a.today_social_counter.split(',')[6])+
                        int(a.today_social_counter.split(',')[7])
                        )

    return render(request, template_name,
    {
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

    area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)

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
        except Exception as inst:
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
            todayVK.append(int(a.today_social_counter.split(',')[0]))
            todayFB.append(int(a.today_social_counter.split(',')[1]))
            todayTW.append(int(a.today_social_counter.split(',')[2]))
            todayOD.append(int(a.today_social_counter.split(',')[3]))
            todayGP.append(int(a.today_social_counter.split(',')[4]))
            todayMA.append(int(a.today_social_counter.split(',')[5]))
            todayLI.append(int(a.today_social_counter.split(',')[6]))
            todayLJ.append(int(a.today_social_counter.split(',')[7]))

        return render(request, template_name,
        {
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
        return HttpResponseRedirect('/webmaster-area/statistic/')

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

    area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)
    
    if area:
        area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        if area_per_day_list.last():
            last_day = area_per_day_list.last()

            if datetime.datetime.now().date() == last_day.date:
                page_detail_list = PageDetail.objects.filter(webmaster_area=area)            
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
        except Exception as inst:
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
            'todayLJ': todayLJ
        })
    else:
        return HttpResponseRedirect('/webmaster-area/statistic/')

@login_required
def delete(request, pk):
    try:
        WebmasterAreaModel.objects.get(pk=pk).delete()
    except Exception as inst:
        pass
    return HttpResponseRedirect('/webmaster-area/')

@login_required
def update(request, pk):
    template_name = 'webmaster_area/update.html'
    title = 'Update webmaster area'
    request_instance = None
    try:
        request_instance = WebmasterAreaModel.objects.get(pk=pk)
    except Exception as inst:
        pass
    if request_instance:
        request_form_data = {
            'name_area': request_instance.name_area,
            'url': request_instance.url,
            'buttons_constructor': request_instance.buttons_constructor
        }
        webmaster_area_form = WebmasterAreaForm(data=request_form_data, user=request.user, instance=request_instance, auto_id=False)
        header = request_instance.name_area
        if request.method == 'POST':
            webmaster_area_form = WebmasterAreaForm(data=request.POST, user=request.user, instance=request_instance)
            if webmaster_area_form.is_valid():
                webmaster_area = webmaster_area_form.save(commit=False)
                webmaster_area.save()
                return HttpResponseRedirect('/webmaster-area/')
                #return render(request, template_name,
                #{
                    #'success': 'Buttons constructor created'
                #})
            else:
                webmaster_area_form = WebmasterAreaForm(buttons_constructor_form.cleaned_data, user=request.user, auto_id=False)
                return render(request, template_name,
                {
                    'page': { 'title': title, 'header': header },
                    'error': webmaster_area_form.errors,
                    'webmaster_area_form': webmaster_area_form
                })
        else:
            #return HttpResponseRedirect('/buttons-constructor/')
            return render(request, template_name,
            {
                'pk': pk,
                'page': { 'title': title, 'header': header },
                'webmaster_area_form': webmaster_area_form
            })
    else:
        return HttpResponseRedirect('/webmaster-area/')

@login_required
def create(request):
    template_name = 'webmaster_area/index.html'
    title = 'Webmaster area'
    header = 'Площадки'
    if request.method == 'POST':
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
            if area.buttons_constructor.cabinet_webmaster.user == request.user:
                user_wma_names_list.append(area.name_area)
            all_wma_urls_list.append(area.url)

        isNameAreaAlreadyExist = request_post_data.get('name_area','') in user_wma_names_list
        isUrlAreaAlreadyExist = urlparse(request_post_data.get('url','')).netloc in all_wma_urls_list

        if webmaster_area_form.is_valid() and isNameAreaAlreadyExist == False and isUrlAreaAlreadyExist == False:

            webmaster_area = webmaster_area_form.save()
            #webmaster_area.buttons_constructor = request.user.cabinet_webmaster.buttons_constructor.all()[0]
            try:
                webmaster_area.buttons_constructor = ButtonsConstructorModel.objects.filter(cabinet_webmaster=request.user.cabinet_webmaster).order_by('-pk')[0]
            except Exception as instance:
                webmaster_area.buttons_constructor = ButtonsConstructorModel.objects.create(cabinet_webmaster=request.user.cabinet_webmaster, btns_images=BtnsImages.objects.latest('pk'))

            webmaster_area.save()

            return HttpResponseRedirect('/webmaster-area/')

    return render(request, template_name,
    {
        "areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
        'page': { 'title': title, 'header': header },
        "ad_type": "Нормальный,Для взрослых",
        "area_category": AreaCategory.objects.all()
    })

def setcounterprivate(url):

    snc = ''
    #url = request.GET.get("url")
    #answer += str(urllib.request.urlopen(url).status)
    if url:
        answer += 'url=' + url + '; '

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
                    html = urllib.request.urlopen(u)
                    response = html.read()
                    response = response.decode('utf8')
                    answer += 'response=' + response + '; '

                    re_result = re.findall(m, response)
                    if len(re_result) > 0:
                        snc += re_result[0] + ','
                    else:
                        snc += '0,'
                except:
                    snc += '0,'

        snc = snc[:-1]

    return snc

def checkconfig(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc
    wma_object = WebmasterAreaModel.objects.filter(url=parsed_referer).last()
    if wma_object:
        answer = ''
        history_referrer = request.GET.get('referrer', 'none referrer')
        history_rr = request.GET.get('rr', 'none rr')
        request_url = request.GET.get('url', 'none url')
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

        #wma!
        #...

        #page detail
        #Disable page_today
        #Total counters in page_detail now work like today counters! They do not collect digits for all time, but update every time then call
        request_url_html = urllib.request.urlopen(request_url)
        soup = BeautifulSoup(request_url_html)

        if parsed_referer == urlparse(request_url).netloc and request_url_html.status == 200:
            answer += 'console.log("url ok");'

            #TODO: snc from server
            answer += 'console.log("snc from client: '+snc+'");'
            try:
                url = request_url
                if url:
                    answer += 'url=' + url + '; '

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
                                html = urllib.request.urlopen(u)
                                response = html.read()
                                response = response.decode('utf8')
                                #answer += 'response=' + response + '; '

                                re_result = re.findall(m, response)
                                if len(re_result) > 0:
                                    snc += re_result[0] + ','
                                else:
                                    snc += '0,'
                            except:
                                snc += '0,'

                    snc = snc[:-1]

                #snc = setcounterprivate(url=request_url)
                answer += 'console.log("snc from server: '+snc+'");'
            except:
                #answer += 'console.log("'+sys.exc_info()[0]+'");'
                pass
            
            #wma today!
            try:
                wma_today = AreaToday.objects.get(webmaster_area=wma_object, date=datetime.date.today())

            except:
                wma_today = AreaToday.objects.create(webmaster_area=wma_object, date=datetime.date.today()) #,today_share_counter=snc)

            try:
                page_detail = PageDetail.objects.get(webmaster_area=wma_object, url=request_url)
                
                if page_detail:
                    page_detail.title = soup.title.string
                    page_detail.total_share_counter = snc

                    if index_sn is not None:
                        short_sn = list_sn[index_sn].shortcut
                        list_sn_shortcuts = [sn.shortcut for sn in list_sn]
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
                        list_sn_shortcuts = [sn.shortcut for sn in list_sn]
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
    answer = 'setcounter() = '
    snc = ''
    url = request.GET.get("url")
    #answer += str(urllib.request.urlopen(url).status)
    if url:
        answer += 'url=' + url + '; '

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
                    html = urllib.request.urlopen(u)
                    response = html.read()
                    response = response.decode('utf8')
                    answer += 'response=' + response + '; '

                    re_result = re.findall(m, response)
                    if len(re_result) > 0:
                        snc += re_result[0] + ','
                    else:
                        snc += '0,'
                except:
                    snc += '0,'

        snc = snc[:-1]

    answer += 'snc=' + snc
    return HttpResponse(snc)
    #return HttpResponse(answer)

def getconfig(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc

    wma_object = WebmasterAreaModel.objects.filter(url=parsed_referer).last()
    if wma_object:

        list_sn = SocialNetworks.objects.all()

        SOCIAL_DEFAULT = ''
        list_sn_unic = {}

        for s in list_sn:
            if not s.shortcut in SOCIAL_DEFAULT:
                SOCIAL_DEFAULT += s.shortcut + ','
                list_sn_unic[s.shortcut] = s

        SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
        btncr = wma_object.buttons_constructor

        answer = 'function sharewallWrapper(){'
        answer += '(function sharewallConstruct($, d, w) {'

        answer += '    $("div#sharewallContainer").html(\'\');'
        if btncr.location_buttons == "VE":
            answer += '$("div#sharewallContainer").css("float","left");'
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

            answer += '$("div#sharewallContainer").append(\'\''
            answer += '   +\'<a data-share-sn="{0}" href=\'+new_href+\' style="width:41px; height:41px; display:inline-block; margin-right:15px; background-image: url(http://sharewall.ru/static/sharewall-template/{1}); background-repeat: no-repeat; {2}"></a>\''.format(sn, btncr.btns_images.path, list_sn_unic[sn].img_bd_pos)#list_sn_img_circle.get(sn) if btncr.form_buttons=='CI' else list_sn_img_square.get(sn))
            if btncr.location_buttons == "VE":
                answer += '+\'<br>\''
            answer += ');'

        answer += '$("div#sharewallContainer").append(\'<a target="_blank" href="//sharewall.ru" style="width:41px; height:41px; display:inline-block; margin-right:15px; background-image: url(http://sharewall.ru/static/sharewall-template/images/btns-logo-sharewall-blue.png); background-repeat: no-repeat; background-position: 50% 50%;"></a>\');'
        if btncr.with_counter:
            if btncr.location_buttons == "VE":
                answer += '$("div#sharewallContainer").append("<br/>");'
            answer += '$("div#sharewallContainer").append(\'<span id="shareCounter" style="margin-left:3px; height:41px; width:64px; display:inline-block; color:#fff; font: 400 14px / 22px Roboto; text-align:center; line-height:41px; vertical-align: top; background-image: url(http://sharewall.ru/static/sharewall-template/images/btns-counter-black.png); background-repeat: no-repeat; background-position: 50% 60%;">0</span>\');'

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
