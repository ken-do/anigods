from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from project.models import ProjectChapterPage, ProjectEpisodePage
from .helpers import unzip_and_remove
import os
from pathlib import Path

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@receiver(post_save, sender=ProjectChapterPage, dispatch_uid="something")
def unzip_chapter(sender, instance, **kwargs):
    zip_chapter_path = PROJECT_DIR + instance.chapter_content.url
    chapters_dir = PROJECT_DIR + os.path.dirname(instance.chapter_content.url)
    zip_file = Path(zip_chapter_path)
    if(zip_file.is_file()):
        unzip_and_remove(zip_chapter_path, chapters_dir)
