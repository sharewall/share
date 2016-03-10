from django.conf.urls import url
from cabinet_webmaster.views import CabinetWebmasterIndexView, settings

urlpatterns = [
    url(r'^$', CabinetWebmasterIndexView.as_view(), name='cabinet-webmaster-index'),
    url(r'^settings/$', settings, name='cabinet-webmaster-settings'),
]
