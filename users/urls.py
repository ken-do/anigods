from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^profile/$', views.profile, name='profile'),
]