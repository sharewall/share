from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^setcounter/$', views.setcounter, name='setcounter'),
    url(r'^getconfig/$', views.getconfig, name='getconfig'),
    url(r'^getconfig2/$', views.getconfig2, name='getconfig2'),
    #url(r'^getconfig2/(?P<title>.+)/$', views.getconfig2, name='getconfig2'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]

