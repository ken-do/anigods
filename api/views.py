from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from anime.models import AnimePage, AnimePageTag
from project.models import ProjectPage, ProjectPageTag
from django.http import Http404, HttpResponse, JsonResponse
# Create your views here.
from django.urls import reverse
from wagtail.search.models import Query

def autoCompleteAPI(request):
    projectTitles = [(project.title, project.url) for project in ProjectPage.objects.all()]
    projectTags = [('Dự án - ' + tag.tag.name.capitalize(), reverse('project:tag', args=(tag.tag.name,))) for tag in ProjectPageTag.objects.all()]

    animeTitles =  [(anime.title, anime.url) for anime in AnimePage.objects.all()]
    animeTags = [( 'Anime - ' + tag.tag.name.capitalize(), reverse('anime:tag', args=(tag.tag.name,))) for tag in AnimePageTag.objects.all()]
    animeStudios = [( 'Studio - ' + anime.studio.name, reverse('anime:studio', args=(anime.studio.slug,))) for anime in AnimePage.objects.all()]
    data = dict([(k,v) for k,v in projectTitles + projectTags + animeTitles + animeTags + animeStudios])

    return JsonResponse(data)   
    