from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.WebmasterAreaIndexView.as_view(), name='webmaster-area-index'),
    url(r'^statistic/$', views.statistic, name='webmaster-area-statistic'),
    url(r'^create/$', views.create, name='webmaster-area-create'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update, name='webmaster-area-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name='webmaster-area-delete'),
    url(r'^detail/(?P<name>[^/]+)/$', views.detail, name='webmaster-area-detail'),
    url(r'^detail-social/(?P<name>[^/]+)/$', views.detailsocial, name='webmaster-area-detail-social'),
    url(r'^detail-main/$', views.detailmain, name='webmaster-area-detail-main'),
    url(r'^setcounter/$', views.setcounter, name='webmaster-area-setcounter'),
    url(r'^getconfig/$', views.getconfig, name='webmaster-area-getconfig'),
    url(r'^checkconfig/$', views.checkconfig, name='webmaster-area-checkconfig'),
    url(r'^detail-error/$', views.detail_error, name='webmaster-area-detail-error'),
    url(r'^thu-may/555/update-server/$', views.updateServer, name='webmaster-area-update-server'),
]

