from django.db import models
from django import forms
from django.db.models import CharField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core.blocks import ( CharBlock, PageChooserBlock, StructBlock, URLBlock)
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.images.blocks import ImageChooserBlock


class SlideBlock(StructBlock):
    heading = CharBlock()
    description = CharBlock()
    background = ImageChooserBlock()
    destination_page = PageChooserBlock(required=False)
    external_url = URLBlock(label="External URL", required=False)   
    button_text = CharBlock()

    class Meta:
        icon = 'form'
        template = 'home/slide.html'

class HomePage(Page):
    slider = StreamField([
        ('slide', SlideBlock()),
    ],default="")

    featured_anime_heading = CharField(max_length=255,default="")
    featured_anime_subheading = CharField(max_length=255,default="")
    featured_anime = StreamField([
        ('anime', PageChooserBlock(icon = 'doc-empty', template = 'home/featured_anime.html', required=False)),
    ],default="",blank=True)
    

    featured_projects_heading = CharField(max_length=255,default="")
    featured_projects_subheading = CharField(max_length=255, default="")
    featured_projects = StreamField([
        ('project', PageChooserBlock(icon = 'doc-full', template = 'home/featured_project.html', required=False)),
    ],default="",blank=True)
    content_panels = Page.content_panels + [
        StreamFieldPanel('slider'),
        MultiFieldPanel([
            FieldPanel('featured_anime_heading'),
            FieldPanel('featured_anime_subheading'),
            StreamFieldPanel('featured_anime'),
            ],
        heading="Featured Anime Section",
        ),
        MultiFieldPanel([
            FieldPanel('featured_projects_heading'),
            FieldPanel('featured_projects_subheading'),
            StreamFieldPanel('featured_projects'),
        ],
        heading="Featured Anime Section",
        )
    ]

