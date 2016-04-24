from django.conf.urls import url
from buttons_constructor.views import ButtonsConstructorIndexView, create, update, delete

urlpatterns = [
    url(r'^$', ButtonsConstructorIndexView.as_view(), name='buttons-constructor-index'),
    url(r'^create/$', create, name='buttons-constructor-create'),
    url(r'^(?P<pk>[0-9]+)/$', update, name='buttons-constructor-update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', delete, name='buttons-constructor-delete'),
]

