from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import ProjectPage
from django.http import Http404, HttpResponse, JsonResponse
# Create your views here.
from django.urls import reverse

from .models import ProjectPageTag
# from .models import ProjectPageCategory as Category
from wagtail.search.models import Query

class TagView(TemplateView):
    template_name = "project/project_filtered_index_page.html"

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dự án thuộc thể loại"
        context['filter_value'] = self.kwargs['tag']
        context['projectpages'] =  ProjectPage.objects.filter(tags__name=self.kwargs['tag'])
        return context
