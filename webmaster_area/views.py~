import datetime, json, os
from urllib.parse import urlparse
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

class WebmasterAreaIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/' 
    template_name = 'webmaster_area/index.html'
    title = 'Webmaster area'
    header = 'Площадки'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        #list_all_user_areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user).order_by('-date')
        #list_distinct, list_distinct_keys = [], []

        #for area in list_all_user_areas:
        #    if area.name_area not in list_distinct_keys:
        #        list_distinct_keys.append(area.name_area)
        #        list_distinct.append(area) 

        return render(request, self.template_name,
        {
            "areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
            #"areas" : list_distinct,
            "page": { "title": self.title, 'header': self.header },
            "ad_type": "Нормальный,Для взрослых",
            "area_category": AreaCategory.objects.all()
            #'webmaster_area_form': WebmasterAreaForm()
        })

@login_required
def statistic(request):
    template_name = 'webmaster_area/statistic.html'
    title = 'Статистика'
    header = 'Статистика'

    #list_all_user_areas = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user)#.order_by('-date')
    #list_distinct, list_distinct_keys = [], []

    #for area in list_all_user_areas:
    #    if area.name_area not in list_distinct_keys:
    #        list_distinct_keys.append(area.name_area)
    #        list_distinct.append(area) 

    return render(request, template_name,
    {
        'areas': WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),
        #"areas" : list_distinct,
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

    area = WebmasterAreaModel.objects.get(buttons_constructor__cabinet_webmaster__user=request.user, name_area=name)
    
    if area:
        area_per_day_list = AreaToday.objects.filter(webmaster_area=area)

        for a in area_per_day_list:
            dates.append(a.date.strftime("%d.%m"))
            todayVK.append(int(a.today_share_counter.split(',')[0]))
            todayFB.append(int(a.today_share_counter.split(',')[1]))
            todayTW.append(int(a.today_share_counter.split(',')[2]))
            todayOD.append(int(a.today_share_counter.split(',')[3]))
            todayGP.append(int(a.today_share_counter.split(',')[4]))
            todayMA.append(int(a.today_share_counter.split(',')[5]))
            todayLI.append(int(a.today_share_counter.split(',')[6]))
            todayLJ.append(int(a.today_share_counter.split(',')[7]))

        return render(request, template_name,
        {
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
    #template_name = 'webmaster_area/create.html'
    #title = 'Create webmaster area'
    #header = 'Создание площадки'
    template_name = 'webmaster_area/index.html'
    title = 'Webmaster area'
    header = 'Площадки'
    if request.method == 'POST':
        #webmaster_area_form = WebmasterAreaForm(data=request.POST, user=request.user, auto_id=False)
        area_category_list = request.POST.getlist('area_category','')
        #todo:
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

        user_wma_list = WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user)
        user_wma_names_list = []
        for area in user_wma_list:
            user_wma_names_list.append(area.name_area)
        isNameAreaAlreadyExist = request_post_data.get('name_area','') in user_wma_names_list

        if webmaster_area_form.is_valid() and isNameAreaAlreadyExist == False:
            webmaster_area = webmaster_area_form.save()
            #webmaster_area.buttons_constructor = request.user.cabinet_webmaster.buttons_constructor.all()[0]
            try:
                webmaster_area.buttons_constructor = ButtonsConstructorModel.objects.filter(cabinet_webmaster=request.user.cabinet_webmaster).order_by('-pk')[0]
            except Exception as instance:
                webmaster_area.buttons_constructor = ButtonsConstructorModel.objects.create(cabinet_webmaster=request.user.cabinet_webmaster, btns_images=BtnsImages.objects.latest('pk'))
            webmaster_area.save()
            return HttpResponseRedirect('/webmaster-area/')
            #return render(request, template_name,
            #{
                #'success': 'Buttons constructor created'
            #})
        else:
            #webmaster_area_form = WebmasterAreaForm(webmaster_area_form.cleaned_data, user=request.user)
            #webmaster_area_form = WebmasterAreaForm(webmaster_area_form.cleaned_data)
            return render(request, template_name,
            {
                "areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
                'page': { 'title': title, 'header': header },
                "ad_type": "Нормальный,Для взрослых",
                "area_category": AreaCategory.objects.all()
                #'error': webmaster_area_form.errors,
                #'webmaster_area_form': webmaster_area_form
            })
    else:
        #return HttpResponseRedirect('/buttons-constructor/')
        return render(request, template_name,
        {
            "areas": WebmasterAreaModel.objects.filter(buttons_constructor__cabinet_webmaster__user=request.user),#.order_by('-date'),
            'page': { 'title': title, 'header': header },
            "ad_type": "Нормальный,Для взрослых",
            "area_category": AreaCategory.objects.all()
            #'webmaster_area_form': WebmasterAreaForm()
            #'webmaster_area_form': WebmasterAreaForm(request.user)
        })

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
        '''
        difference_share_counter = ''
        for s,s2 in zip(snc.split(','), wma_object.total_share_counter.split(',')):
            difference_share_counter += str(int(s) - int(s2)) + ','
        difference_share_counter = difference_share_counter[:-1]
        new_today_social_counter = ''
        new_today_share_counter = ''
        for s,s2 in zip(wma_object.today_share_counter.split(','), difference_share_counter.split(',')):
            new_today_social_counter += '0,'
            new_today_share_counter += str(int(s) + int(s2)) + ','
        new_today_social_counter = new_today_social_counter[:-1]
        new_today_share_counter = new_today_share_counter[:-1]
        new_total_social_counter = wma_object.total_social_counter
        update_today_social_counter = wma_object.today_social_counter
        '''
        wma_today = AreaToday.objects.get(webmaster_area=wma_object,date=datetime.date.today())
        if wma_today:
            wma_today.today_share_counter = snc
            wma_today.save()
            answer += 'console.log("'+str(wma_today) + ' updated!");' 
        else:
            wma_today = AreaToday.objects.create(webmaster_area=wma_object,date=datetime.date.today(),today_share_counter=snc)
            answer += 'console.log("'+str(wma_today) + ' created!");' 

        if index_sn is not None:
            short_sn = list_sn[index_sn].shortcut
            list_sn_shortcuts = [sn.shortcut for sn in list_sn]
            index_sn = list_sn_shortcuts.index(short_sn)

            '''
            temp_li_today_sn = [int(s) for s in new_today_social_counter.split(',')]
            temp_li_total_sn = [int(s) for s in new_total_social_counter.split(',')]
            temp_li_update_today_sn = [int(s) for s in update_today_social_counter.split(',')]
            temp_li_today_sn[index_sn] += 1
            temp_li_total_sn[index_sn] += 1
            temp_li_update_today_sn[index_sn] += 1
            new_today_social_counter = ''
            new_total_social_counter = ''
            update_today_social_counter = ''
            for i in temp_li_today_sn:
                new_today_social_counter += str(i) + ','
            for i in temp_li_total_sn:
                new_total_social_counter += str(i) + ','
            for i in temp_li_update_today_sn:
                update_today_social_counter += str(i) + ','
            new_today_social_counter = new_today_social_counter[:-1]
            new_total_social_counter = new_total_social_counter[:-1]
            update_today_social_counter = update_today_social_counter[:-1]
            '''

        '''
        if wma_object.date == datetime.date.today():
            wma_object.today_share_counter = new_today_share_counter
            wma_object.total_share_counter = snc
            wma_object.today_social_counter = update_today_social_counter
            wma_object.total_social_counter = new_total_social_counter
            wma_object.save()
            answer += 'console.log("'+str(wma_object) + ' updated!");' 
        else:
            wma_object = WebmasterAreaModel.objects.create(buttons_constructor = wma_object.buttons_constructor, name_area = wma_object.name_area, url=wma_object.url, today_social_counter=new_today_social_counter, total_social_counter=new_total_social_counter, today_share_counter=difference_share_counter, total_share_counter=snc)
            answer += 'console.log("'+str(wma_object) + ' created!");' 
        '''
        #page_detail, created = PageDetail.objects.get_or_create(webmaster_area=wma_object, url=request_url, defaults={'': 1, 'title': request_title})
        #if not created:
            #page_detail.page_social_traffic += 1
            #page_detail.title = request_title
            #page_detail.save()
        #answer += 'snc = %s'%snc
        #answer = '    console.log("%s'%history_referrer+' != %s'%history_rr+'");\n'
        answer += '    document.cookie = "_sharewallrr=; expires=Thu, 01 Jan 1970 00:00:00 UTC";'
        answer += '    var date = new Date(); date.setTime(date.getTime() + 24*60*60*1000);'
        answer += '    document.cookie = "_sharewallrr=%s'%history_referrer+'; path=%s'%urlparse(request_url).path+'; max-age="+24*60*60+"; expires="+date.toGMTString();'
    else:
        answer = 'bad id!'
    return HttpResponse(answer)

def setcounter(request):
    return HttpResponse('setcounter')
    '''
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc
    wma_object = WebmasterAreaModel.objects.filter(url=parsed_referer).last()
    if wma_object:
        if wma_object.date == datetime.date.today():
            wma_object.share_today_counter += 1
            wma_object.share_total_counter += 1
            wma_object.save()
            answer = 'console.log("'+str(wma_object) + ' updated!")' 
        else:
            wma_object = WebmasterAreaModel.objects.create(buttons_constructor = wma_object.buttons_constructor, name_area = wma_object.name_area, url=wma_object.url, share_today_counter=1, share_total_counter=wma_object.share_total_counter+1)
            answer = 'console.log("'+str(wma_object) + ' created!")' 

        request_url = request.GET.get('url', 'none url')
        request_title = request.GET.get('title', 'none title')
        page_detail, created = PageDetail.objects.get_or_create(webmaster_area=wma_object, url=request_url, defaults={'page_share_counter': 1, 'title': request_title})
        if not created:
            page_detail.page_share_counter += 1
            page_detail.title = request_title
            page_detail.save()
    else:
        answer = 'console.log(bad id!)' 
    return HttpResponse(answer)
    '''

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
        #list_sn_img_square = {sn.shortcut: sn.img_square for sn in list_sn}
        #list_sn_img_circle = {sn.shortcut: sn.img_circle for sn in list_sn}
        btncr = wma_object.buttons_constructor
        #dict_config = {}
        #if btncr.with_counter:
            #dict_config['counter'] = wma_object.total_share_counter
        #if btncr.with_background:
            #dict_config['background'] = btncr.background_color
        #if btncr.page_url:
            #dict_config['url'] = btncr.page_url
        #if btncr.page_title:
            #dict_config['title'] = btncr.page_title
        #if btncr.page_description:
            #dict_config['description'] = btncr.page_description
        #dict_config['mob-view'] = btncr.mobile_view
        #dict_config['social'] = btncr.social_networks
        #dict_config['form'] = btncr.get_form_buttons_display()
        #dict_config['location'] = btncr.get_location_buttons_display()
        #dict_config['size'] = btncr.get_size_buttons_display()
        #response_config = json.dumps(dict_config, sort_keys=True, indent=0)

        answer = 'function sharewallWrapper(){'
        answer += '(function sharewallConstruct($, d, w) {'
        #answer += '    sharewall = { };'
        #answer += '    sharewall = { share_config: %s};' %response_config
        #answer += '    console.log(sharewall.share_config); '

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
        })(jQuery, document, window)'
        answer += '}'
        answer += 'if(jQuery){\
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
