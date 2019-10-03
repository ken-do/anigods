from django.conf.urls import url
from . import views

app_name = 'anime'

urlpatterns = [
    url(r'^tag/(?P<tag>((?:\w+-*)+\w+))/$', views.TagView.as_view(), name='tag'),
    url(r'^studio/(?P<studio>((?:\w+-*)+\w+))/$', views.StudioView.as_view(), name='studio'),
    url(r'^release/(?P<season>\w+)/(?P<year>\w+)/$', views.ReleaseTimeView.as_view(), name='release_time'),
    url(r'^format/(?P<format>((?:\w+-*)+\w+))/$', views.FormatView.as_view(), name='format'),
]