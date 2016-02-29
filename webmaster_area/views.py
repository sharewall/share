from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from webmaster_area.models import WebmasterAreaModel, PageDetail
from buttons_constructor.models import SocialNetworks
from urllib.parse import urlparse
import datetime
import json
import os

def index(request):
    return HttpResponse("webmaster-area")

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
        answer += 'console.log("%s");'%history_parsed_referrer
        if history_referrer != history_rr and history_parsed_referrer in list_parsed_sn:
            index_sn = list_parsed_sn.index(history_parsed_referrer)
            answer += 'console.log("list_parsed = {0} history_parsed_referrer = {1} index = {2} history_rr = {3} history_referrer = {4}");'.format(list_parsed_sn, history_parsed_referrer, index_sn, history_rr, history_referrer)
        #wma!
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
        if index_sn is not None:
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

def getconfig(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc
    wma_object = WebmasterAreaModel.objects.filter(url=parsed_referer).last()
    if wma_object:
        list_sn = SocialNetworks.objects.all()
        SOCIAL_DEFAULT = ''
        for s in list_sn:
            if not s.shortcut in SOCIAL_DEFAULT:
                SOCIAL_DEFAULT += s.shortcut + ','
        SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
        list_sn_img_square = {sn.shortcut: sn.img_square for sn in list_sn}
        list_sn_img_circle = {sn.shortcut: sn.img_circle for sn in list_sn}
        btncr = wma_object.buttons_constructor
        dict_config = {}
        if btncr.with_counter:
            dict_config['counter'] = wma_object.total_share_counter
        if btncr.with_background:
            dict_config['background'] = btncr.background_color
        if btncr.page_url:
            dict_config['url'] = btncr.page_url
        if btncr.page_title:
            dict_config['title'] = btncr.page_title
        if btncr.page_description:
            dict_config['description'] = btncr.page_description
        dict_config['mob-view'] = btncr.mobile_view
        dict_config['social'] = btncr.social_networks
        dict_config['form'] = btncr.get_form_buttons_display()
        dict_config['location'] = btncr.get_location_buttons_display()
        dict_config['size'] = btncr.get_size_buttons_display()
        response_config = json.dumps(dict_config, sort_keys=True, indent=0)

        answer = 'function sharewallWrapper(){'
        answer += '(function sharewallConstruct($, d, w) {'
        answer += '    sharewall = { share_config: %s};' %response_config
        answer += '    console.log(sharewall.share_config); '

        answer += '    $("div#sharewallContainer").html(\'\''
        if btncr.with_counter:
            answer += '    +\'<span id="shareCounter" style="padding: 4px 8px; border: 0px none; background-color: rgb(91, 192, 222); border-radius: 4px;  color: white;">0</span>\''
        if btncr.with_counter and btncr.location_buttons == "VE":
            answer += '+\'<br>\''
        answer += ');'

        for sn in btncr.social_networks.split(','):
            answer += 'var new_href = "";'
            if sn == 'vk':
                answer += 'new_href = "http://vk.com/share.php?url="+{0}+{1}+{2}+{3};'.format(
                    'encodeURIComponent('+btncr.page_url+')' if btncr.page_url else 'encodeURIComponent(d.URL)',
                    '"&description="+encodeURIComponent('+btncr.page_description+')' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&description="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&title="+encodeURIComponent(d.title)',
                    '"&noparse=true"'
                )
            if sn == "fb":
                answer += 'new_href = "https://www.facebook.com/sharer/sharer.php?s=100"+{0}+{1}+{2};'.format(
                    '"&p[url]="+encodeURIComponent('+btncr.page_url+')' if btncr.page_url else '"&p[url]="+encodeURIComponent(d.URL)',
                    '"&p[summary]="+encodeURIComponent('+btncr.page_description+')' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&p[summary]="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&p[title]="+encodeURIComponent(d.title)'
                )
            if sn == "tw":
                answer += 'new_href = "https://www.twitter.com/share?"+{0}+{1};'.format(
                    '"url="+encodeURIComponent('+btncr.page_url+')' if btncr.page_url else '"url="+encodeURIComponent(d.URL)',
                    '"&text="+encodeURIComponent(d.title)'
                )
            if sn == "od":
                answer += 'new_href = "http://www.odnoklassniki.ru/dk?st.cmd=addShare&st.s=1"+{0}+{1};'.format(
                    '"&st._surl="+encodeURIComponent('+btncr.page_url+')' if btncr.page_url else '"&st._surl="+encodeURIComponent(d.URL)',
                    '"&st.comments="+encodeURIComponent('+btncr.page_description+')' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&st.comments="+encodeURIComponent(d.head.children.Description.content) : "")'
                )
            if sn == "gp":
                answer += 'new_href = "https://plus.google.com/share?"+{0};'.format(
                    '"url="+encodeURIComponent('+btncr.page_url+')' if btncr.page_url else '"url="+encodeURIComponent(d.URL)'
                )
            if sn == "ma":
                answer += 'new_href = "http://connect.mail.ru/share?"+{0}+{1}+{2};'.format(
                    '"url="+encodeURIComponent('+btncr.page_url+')' if btncr.page_url else '"url="+encodeURIComponent(d.URL)',
                    '"&description="+encodeURIComponent('+btncr.page_description+')' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&description="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&title="+encodeURIComponent(d.title)'
                )
            if sn == "li":
                answer += 'new_href = "http://www.linkedin.com/shareArticle?mini=true"+{0}+{1}+{2};'.format(
                    '"&url="+encodeURIComponent('+btncr.page_url+')' if btncr.page_url else '"&url="+encodeURIComponent(d.URL)',
                    '"&summary="+encodeURIComponent('+btncr.page_description+')' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "&summary="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&title="+encodeURIComponent(d.title)'
                )
            if sn == "lj":
                answer += 'new_href = "http://www.livejournal.com/update.bml?"+{0}+{1};'.format(
                    '"event="+encodeURIComponent('+btncr.page_description+')' if btncr.page_description else '(typeof d.head.children.Description != "undefined" ? "event="+encodeURIComponent(d.head.children.Description.content) : "")',
                    '"&subject="+encodeURIComponent(d.title)'
                )

            answer += '$("div#sharewallContainer").append(\'\''
            answer += '   +\'<a data-share-sn="{0}" href=\'+new_href+\'><img src="{1}" alt="{0}" title="{0}" align="middle" border="0" height="28" hspace="0" width="28"></a>\''.format(sn, list_sn_img_circle.get(sn) if btncr.form_buttons=='CI' else list_sn_img_square.get(sn))
            if btncr.location_buttons == "VE":
                answer += '+\'<br>\''
            answer += ');'

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
        #answer += '    $.when($.ajax({ url: "http://anyorigin.com/get?callback=?&url=" + encodeURIComponent("https://plusone.google.com/u/0/_/+1/fastbutton?count=true&url=" + d.URL), dataType: "json", success: function(response) { sharewallSetSNC("gp", $(response.contents).find("#aggregateCount").html()); }\
        #               })\
        #               ).then(w.setTimeout(function(){\
        #               console.log("GP init setTimeout=20000");\
        #               $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
        #               },20000));'
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
                           $.ajax({ url: "http://connect.mail.ru/share_count?url_list="+encodeURIComponent(document.URL)+"&callback=1&func=sharewallMyMailCallback", dataType: "jsonp", jsonp: false }),\
                           $.ajax({ url: "https://www.linkedin.com/countserv/count/share?url=" + encodeURIComponent(d.URL), dataType: "jsonp", success: function(response) { sharewallSetSNC("li", response.count); }\
                           })\
                       ).done(w.setTimeout(function(){\
                       console.log("done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));'

        answer += ' $("div#sharewallContainer").children().each(\
            function(i,e){\
                $this = $(e);\
                if($this.is("a")){\
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
                       $.when($.ajax({ url: "http://connect.mail.ru/share_count?url_list="+encodeURIComponent(document.URL)+"&callback=1&func=sharewallMyMailCallback", dataType: "jsonp", jsonp: false })\
                       ).done(w.setTimeout(function(){\
                       console.log("MA done setTimeout=1000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },1000));\
                    }'
        answer += 'if(sn=="gp"){\
                       $.when($.ajax({ url: "http://anyorigin.com/get?callback=?&url=" + encodeURIComponent("https://plusone.google.com/u/0/_/+1/fastbutton?count=true&url=" + d.URL), dataType: "json", success: function(response) { sharewallSetSNC("gp", $(response.contents).find("#aggregateCount").html()); }\
                        })\
                       ).then(w.setTimeout(function(){\
                       console.log("GP done setTimeout=20000");\
                       $.ajax({ url: "http://sharewall.ru/webmaster-area/checkconfig", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title, rr: d.cookie.replace(/(?:(?:^|.*;\s*)_sharewallrr\s*\=\s*([^;]*).*$)|^.*$/, "$1"), snc: sharewallGetAllSNC() } });\
                       },20000));\
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
