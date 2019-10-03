from django.db import models
from django import forms

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel,FieldRowPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator

from .storage import OverwriteStorage



@register_snippet
class ProjectAuthor(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('avatar'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProjectPage',
        related_name='tagged_items',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
       return self.name


class ProjectIndexPage(Page):
    intro = models.CharField(max_length=300)
    layout = models.CharField(max_length=300, default="grid-4-cols")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('layout'),
        ImageChooserPanel('featured_image')
    ]

  

class ProjectPage(Page):

    # Database fields
    intro = models.CharField(max_length=400, null=True, blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ],
        default="")
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_context(self, request):
        context = super().get_context(request)
        context['project_chapter'] = ProjectChapterPage.objects.child_of(self).live()
        context['project_episode'] = ProjectEpisodePage.objects.child_of(self).live()
        return context

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('tags'),
        ], heading="Meta Info"),
        ImageChooserPanel('featured_image'),

    ]


    # Parent page / subpage type rules

    parent_page_types = ['project.ProjectIndexPage']


def chapter_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'project_resources/manga/{0}/{1}'.format(instance.get_parent().slug, filename)

class ProjectChapterPage(Page):
    chapter_number = models.CharField(max_length=4, default=1)
    chapter_content = models.FileField(upload_to=chapter_upload_path, null=True, blank=True)

    content_panels =  Page.content_panels + [
        FieldRowPanel([
            FieldPanel('chapter_number', classname="col7"),
            FieldPanel('chapter_content', classname="col7")
        ], 'Chapter Info')
    ]

    parent_page_types = ['project.ProjectPage']
    
    def __str__(self):
       return self.title

def episode_upload_path(instance, filename):
    return 'project_resources/anime/{0}/{1}'.format(instance.get_parent().slug, filename)

class ProjectEpisodePage(Page):
    episode_number = models.CharField(max_length=4, default=1)
    episode_featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    episode_video = models.FileField(upload_to=episode_upload_path, storage=OverwriteStorage(), null=True, blank=True)


    content_panels = Page.content_panels +  [
        FieldPanel('episode_number'),
        ImageChooserPanel('episode_featured_image'),
        FieldPanel('episode_video', classname="col12")
    ]

    parent_page_types = ['project.ProjectPage']


    def __str__(self):
       return self.title