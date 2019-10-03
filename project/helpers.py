import zipfile
import os, glob, re
from project.models import ProjectChapterPage

def unzip_and_remove(zip_file, destination, **kwargs):
    """
    Args:
        zip_folder (string): zip folder to be unzipped
        destination (string): path of destination folder
        pwd(string): zip folder password
    """
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(destination)
    os.remove(zip_file)

def update_images_total(dir, chapter_number, chapter_parent):
    images_list = os.listdir(dir) # dir is your directory path
    images_total = len(images_list)
    ProjectChapterPage.objects.descendant_of(chapter_parent).filter(chapter_number=chapter_number).update(chapter_total_images=images_total)

    

# def rename_chapter_images(dir, pattern, zip_chapter_path):
#     chapter_pattern = re.compile(r"/chap-(?P<chapter>[0-9]+\-?[0-9]?)")
#     number_group = chapter_pattern.search(zip_chapter_path)
#     chapter = number_group['chapter']
#     # sub_number = number_group['sub_number']
#     count = 0

#     for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
#         title, ext = os.path.splitext(os.path.basename(pathAndFilename))
#         # if not sub_number:
#         output_name = "chap-{}_{:03d}".format(chapter, count)
#         # else:
#         #     output_name = "chap-{:03d}-{:d}_{:03d}".format(int(chapter), int(sub_number), count)
        
#         os.rename(pathAndFilename, os.path.join(dir, output_name + ext))
#         count+=1
