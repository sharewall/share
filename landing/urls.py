from django.conf.urls import url
from landing.views import LandingView, landing, register, login, logout, admin_webmasters, admin_change_status, admin_profile, admin_profile_clear, admin_area_by_id, chat, chat_create, admin_chat_billing, admin_chat_support, chat_update, admin_wm_by_id

#app_name = 'landing'
urlpatterns = [
    url(r'^$', landing, name='landing-index'), #LandingView.as_view(), name='landing-index'),
    url(r'^register/$', register, name='landing-register'),
    url(r'^login/$', login, name='landing-login'),
    url(r'^logout/$', logout, name='landing-logout'),
    url(r'^chat/(?P<pk>[0-9]+)/$', chat_update, name='chat-update'),
    url(r'^chat/$', chat, name='chat-all'),
    url(r'^chat/create/$', chat_create, name='chat-create'),
    url(r'^admin/webmasters/$', admin_webmasters, name='admin-webmasters'),
    url(r'^admin/change-status/$', admin_change_status, name='admin-change-status'),
    url(r'^admin/profile/(?P<pk>[0-9]+)/$', admin_profile, name='admin-profile'),
    url(r'^admin/profile-clear/$', admin_profile_clear, name='admin-profile-clear'),
    url(r'^admin/area-by-id/$', admin_area_by_id, name='admin-area-by-id'),
    url(r'^admin/chat/billing/$', admin_chat_billing, name='admin-chat-billing'),
    url(r'^admin/chat/support/$', admin_chat_support, name='admin-chat-support'),
    url(r'^admin/wm-by-id/$', admin_wm_by_id, name='admin-wm-by-id'),
]
