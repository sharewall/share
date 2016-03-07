from django.conf.urls import url
from buttons_constructor.views import ButtonsConstructorIndexView

urlpatterns = [
    url(r'^$',ButtonsConstructorIndexView.as_view(), name='buttons-constructor-index'),
    #url(r'^(?P<pk>[0-9]+)/$', LandingAboutView.as_view(), name='about_landing'),
]

