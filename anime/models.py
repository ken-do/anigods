import datetime

from django.db import models
from django import forms

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


@register_snippet
class AnimeStudio(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255,null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Studios'


class AnimePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'AnimePage',
        related_name='tagged_items',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
       return self.name



class AnimeIndexPage(Page):
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

class AnimePage(Page):

     # Database fields
    intro = models.CharField(max_length=450, null=True, blank=True)
    body = StreamField(
        [
            ('heading', blocks.CharBlock(classname="full title")),
            ('paragraph', blocks.RichTextBlock()),
            ('image', ImageChooserBlock())
        ],
        default=""  
        )
    
    studio = models.ForeignKey('anime.AnimeStudio',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='studio')
    
    format = models.CharField(
        max_length=20,
        choices=[
            ('tv-series', 'TV Series'),
            ('ova', 'OVA'),
            ('movie', 'MOVIE'),
            ],
        default='tv-series',
    )

    season = models.CharField(
        max_length=6,
        choices=[
            ('spring', 'Spring'),
            ('summer', 'Summer'),
            ('autumn', 'Autumn'),
            ('winter''', 'Winter'),           
            ],
        default='spring',
    )
    now = datetime.datetime.now()
    year = models.IntegerField(validators=[MinValueValidator(1950),MaxValueValidator(2050)], default = now.year)
    tags = ClusterTaggableManager(through=AnimePageTag, blank=True)
    # categories = ParentalManyToManyField('project.ProjectPageCategory', blank=True)
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('tags'),
            # FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Meta Info"),
        FieldRowPanel([
            FieldPanel('studio', classname="col3"),
            FieldPanel('format', classname="col3"),
            FieldPanel('season', classname="col3"),
            FieldPanel('year', classname="col3"),
            ]),
        ImageChooserPanel('featured_image'),

    ]
    # Parent page / subpage type rules

    parent_page_types = ['anime.AnimeIndexPage']