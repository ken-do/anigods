from django import template
register = template.Library()

from project.models import ProjectChapterPage, ProjectEpisodePage

register = template.Library()

@register.simple_tag(takes_context=True)
def get_latest_chapters(context):
    return ProjectChapterPage.objects.live().order_by('-first_published_at')[:4]

@register.simple_tag(takes_context=True)
def get_latest_episodes(context):
    return ProjectEpisodePage.objects.live().order_by('-first_published_at')[:4]