from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import AnimePage
from django.http import Http404, HttpResponse, JsonResponse
# Create your views here.
from django.urls import reverse
from wagtail.search.models import Query

# Create your views here.

class TagView(TemplateView):
    template_name = "anime/anime_filtered_index_page.html"

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['title'] = "Anime thuộc thể loại"
        context['filter_type'] = "tag"
        context['filter_value'] = self.kwargs['tag']
        context['animepages'] =  AnimePage.objects.filter(tags__name=self.kwargs['tag'])
        return context


class StudioView(TemplateView):
    template_name = "anime/anime_filtered_index_page.html"

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['title'] = "Anime được sản xuất bởi"
        context['filter_type'] = "studio"
        context['filter_value'] =  self.kwargs['studio'].replace('-',' ')
        context['animepages'] =  AnimePage.objects.filter(studio__slug=self.kwargs['studio'])
        return context


class ReleaseTimeView(TemplateView):
    template_name = "anime/anime_filtered_index_page.html"

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['title'] = "Anime được phát hành vào"
        context['filter_type'] = "release_time"
        context['filter_value'] = self.kwargs['season'] + " " + self.kwargs['year']
        context['animepages'] =  AnimePage.objects.filter(season=self.kwargs['season'],year=self.kwargs['year'])
        return context

class FormatView(TemplateView):
    template_name = "anime/anime_filtered_index_page.html"

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['title'] = "Anime được phát hình dưới hình thức"
        context['filter_type'] = "format"
        context['filter_value'] =  self.kwargs['format']
        context['animepages'] =  AnimePage.objects.filter(format=self.kwargs['format'])
        return context
