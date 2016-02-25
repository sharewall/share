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

def getconfig2(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc
    wma_object = WebmasterAreaModel.objects.filter(url=parsed_referer).last()
    if wma_object:
        response = HttpResponse("console.log('%s"%parsed_referer+" == %s"%wma_object.url+"')")
    else:
        response = HttpResponse("console.log('%s"%parsed_referer+"')")
    return response

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
        answer = 'console.log(Bad url!)' 
    return HttpResponse(answer)

def getconfig(request):
    request_referer = request.META.get('HTTP_REFERER')
    parsed_referer = urlparse(request_referer).netloc
    wma_object = WebmasterAreaModel.objects.filter(url=parsed_referer).last()
    if wma_object:
        request_referrer = request.GET.get('referrer', 'none referrer')
        request_rr = request.GET.get('rr', 'none rr')
        answer = ''
        if request_referrer != request_rr:
            #answer += '    console.log("%s'%request_referrer+' != %s'%request_rr+'");\n'
            parsed_referrer = urlparse(request_referrer).netloc
            list_parsed_sn = [urlparse(sn.url).netloc for sn in SocialNetworks.objects.all()]
            if parsed_referrer in list_parsed_sn:
                request_url = request.GET.get('url', 'none url')
                request_title = request.GET.get('title', 'none title')
                page_detail, created = PageDetail.objects.get_or_create(webmaster_area=wma_object, url=request_url, defaults={'page_social_traffic': 1, 'title': request_title})
                if not created:
                    page_detail.page_social_traffic += 1
                    page_detail.title = request_title
                    page_detail.save()

        btncr = wma_object.buttons_constructor
        dict_config = {}
        if btncr.with_counter:
            dict_config['counter'] = wma_object.share_total_counter
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
        response_config = json.dumps(dict_config, sort_keys=True, indent=12)

        answer += "(function shareITConstruct($, d, w) {\n"
        answer += '    document.cookie = "_rr=; expires=Thu, 01 Jan 1970 00:00:00 UTC";\n'
        answer += '    var date = new Date();\n    date.setTime(date.getTime() + 30*60*1000);\n'
        answer += '    document.cookie = "_rr=%s'%request_referrer+'; path=%s'%request_referrer+'; max-age=60*30; expires=date.toGMTString()";\n'
        answer += "    shareIT = { \n        share_config: %s};\n" %response_config
        answer += "    console.log(shareIT.share_config);\n"
        answer += "window.VK = { Share: { count: function(index, counter){ console.log(counter); "
        answer += '    count = $("div#shareITContainer").find("span#shareCounter").text(); '
        answer += ' if(parseInt(counter) > parseInt(count)){'
        answer += '    $.ajax({ url: "http://sharewall.ru/webmaster-area/setcounter/", dataType: "jsonp", jsonp: false, data: { referrer: d.referrer, url: d.URL, title: d.title } });'
        #answer += 'count = (parseInt(count)+1);\
        answer += ' $("div#shareITContainer").find("span#shareCounter").text(counter);'
        answer += ' }'
        answer += "} }  };"
        answer += '    $("div#shareITContainer").html(\''
        if btncr.with_counter:
            answer += '    <span id="shareCounter" style="padding: 4px 8px; border: 0px none; background-color: rgb(91, 192, 222); border-radius: 4px;  color: white;">%s'%wma_object.share_total_counter+'</span>\''
        else:
            answer += '\''
        if btncr.location_buttons == "VE":
            if btncr.with_counter:
                answer += '+\'<br>\''
            else:
                answer += ''
        else:
            answer += ''
        answer += '   +\'<a data-share-sn="vk" href=""><img src="http://services.google.com/fh/files/misc/vkontakte.png" alt="VK" title="VK" align="middle" border="0" height="28" hspace="0" width="28"></a>\'\n'
        if btncr.location_buttons == "VE":
            answer += '+\'<br>\''
        answer += '    +\'<a data-share-sn="fb" href=""><img src="https://googleru.i.lithium.com/html/assets/facebook_icon_set.png" alt="Facebook" title="Facebook" align="middle" border="0" height="28" hspace="0" width="28"></a>\');\n'
        answer += '    $("div#shareITContainer").children().each(function(i,e){ $this = $(e); if($this.is("a")){ sn = $this.data("shareSn"); new_href = ""; new_title = "%s'%btncr.page_title+'"; new_desc = "%s'%btncr.page_description+'"; new_url = "%s'%btncr.page_url+'"; share_img = ""; $("img").each(function(i,e){ if(e.id == "share_img"){ share_img = e.src; } }); if (typeof d.head.children.Description != "undefined" && !new_desc){ new_desc = d.head.children.Description.content; } if(sn=="vk"){ new_href="http://vk.com/share.php?" + (new_url ? "url=" + encodeURIComponent(new_url) : "url=" + encodeURIComponent(d.URL)) + (new_desc ? "&description=" + encodeURIComponent(new_desc) : "") + (new_title ? "&title=" + encodeURIComponent(new_title) : "&title=" + encodeURIComponent(d.title)) + "&image=" + encodeURIComponent(share_img) + "&noparse=true"; }  $this.attr("href", new_href); return false; }});'
        answer += '    $("div#shareITContainer").children().each(function(i,e){ if($(e).is("a")){ $(e).click( function() { $this = $(this); new_window = w.open($this.attr("href"), "", "left=0,top=0,personalbar=0,scrollbars=1,resizable=1,toolbar=0,width=626,height=436"); var popup_w_interval = w.setInterval(function() {'
        answer += '    console.log("popup opened...");\
        if (new_window.closed !== false) {\
            w.clearInterval(popup_w_interval);\
            console.log("popup closed!");'
        answer += 'jQuery.ajax({ url: "http://vk.com/share.php?act=count&url="+encodeURIComponent(d.URL), dataType: "jsonp" });'

        answer += '   }}, 900); return false; }); }});\
})(jQuery, document, window)'
        path = os.path.join(settings.BASE_DIR, 'webmaster_area')
        path_to_file = os.path.join(path, 'script.js')
        response_script = ''
        #TODO: from .js move here
        with open(path_to_file, 'r') as f:
            for l in f:
                response_script += l

        answer += "\n" + response_script
    else:
        answer = 'console.log(Bad url!)' 
    return HttpResponse(answer, content_type='application/javascript')
