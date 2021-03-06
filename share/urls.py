"""share URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'sharewall.ru administration'
admin.site.site_title = 'fruitbag.ru administration'

#urlpatterns = patterns('',
    #(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
#)

urlpatterns = [
    url(r'^', include('landing.urls')),
    url(r'^share-admin/', admin.site.urls),
    url(r'^buttons-constructor/', include('buttons_constructor.urls')),
    url(r'^cabinet-webmaster/', include('cabinet_webmaster.urls')),
    url(r'^webmaster-area/', include('webmaster_area.urls')),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += patterns('', 
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)
