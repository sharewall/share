from django.conf.urls import url
from landing.views import LandingView, register, login, logout

#app_name = 'landing'
urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing-index'),
    url(r'^register/$', register, name='landing-register'),
    url(r'^login/$', login, name='landing-login'),
    url(r'^logout/$', logout, name='landing-logout'),
]
