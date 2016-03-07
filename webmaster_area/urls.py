from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='webmaster-area-index'),
    url(r'^setcounter/$', views.setcounter, name='webmaster-area-setcounter'),
    url(r'^getconfig/$', views.getconfig, name='webmaster-area-getconfig'),
    url(r'^checkconfig/$', views.checkconfig, name='webmaster-area-checkconfig'),
    #url(r'^getconfig2/(?P<title>.+)/$', views.getconfig2, name='getconfig2'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]

