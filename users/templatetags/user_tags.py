from django import template
import datetime

register = template.Library()

@register.filter()
def more_than_60_days(date):
    print(date)
    if (not date):
        return True
    else:
        delta = datetime.date.today() - date
        return delta.days >= 60