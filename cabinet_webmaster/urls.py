from django.conf.urls import url
from cabinet_webmaster.views import CabinetWebmasterIndexView

urlpatterns = [
    url(r'^$', CabinetWebmasterIndexView.as_view(), name='cabinet-webmaster-index'),
]
