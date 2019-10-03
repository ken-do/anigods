from django import template
from datetime import datetime, timezone
import os

register = template.Library()

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@register.filter() 
def times(number):
    return range(number)


@register.filter() 
def plus_one(number):
    return int(number) + 1


@register.filter() 
def minus_one(number):
    return int(number) - 1


@register.filter()
def to_int(value):
    return int(value)

@register.filter() 
def to_ago(lastTime):
    currentTime = datetime.now(timezone.utc)
    if(lastTime):
        delta = currentTime - lastTime
    else:
        delta = currentTime - currentTime

    days, hours, mins, secs = delta.days, delta.seconds//3600, (delta.seconds//60)%60, delta.seconds
    if(days == 1):
        return  str(days) + ' day ago'
    elif (days):
        return str(days) + ' days ago'
    elif (hours == 1):
        return str(hours) + ' hour ago'
    elif (hours):
        return str(hours) + ' hours ago'
    elif (mins == 1):
        return str(mins) + ' minute ago'
    elif (mins):
        return str(mins) + ' minutes ago'
    elif (secs == 1):
        return str(secs) + ' second ago'
    elif(secs):
        return str(secs) + ' seconds ago'
    else:
        return lastTime

@register.filter()
def get_total_images(chapter_url):
    print(PROJECT_DIR)
    dir = PROJECT_DIR + chapter_url.split('.')[0]
    print(dir)
    list = os.listdir(dir) # dir is your directory path
    number_files = len(list)
    return number_files


@register.simple_tag(takes_context=True)
def get_latest_projects(context, project_type):
    return ProjectPage.objects.live().order_by('last_published_at')[:4]
