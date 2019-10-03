from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [
    url(r'^autocomplete/$', views.autoCompleteAPI, name='autocomplete'),
]