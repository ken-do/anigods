from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [
    url(r'^tag/(?P<tag>((?:\w+-*)+\w+))/$', views.TagView.as_view(), name='tag'),
]