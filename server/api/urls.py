from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as rest_framework_auth_views

app_name = 'api'

urlpatterns = [
    url(r'auth/register/$', views.auth_register, name='auth_register'),
    url(r'auth/login/$', views.auth_login, name='auth_login'),
    url(r'auth/logout/$', views.auth_logout, name='auth_logout'),
    url(r'auth/token/$', rest_framework_auth_views.obtain_auth_token,
        name='auth_token'),
    url(r'track/$', views.track),
    url(r'analytics/consolidated/$', views.analytics_consolidated),
    url(r'analytics/top/pages/$', views.analytics_top_pages),
    url(r'analytics/top/countries/$', views.analytics_top_countries),
    url(r'analytics/top/browsers/$', views.analytics_top_browsers),
    url(r'analytics/top/screen_resolutions/$',
        views.analytics_top_screen_resolutions),
    url(r'analytics/graph/$', views.analytics_graph),
]
