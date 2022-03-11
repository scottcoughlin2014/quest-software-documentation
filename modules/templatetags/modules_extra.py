from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def makedash(value):
    return value.replace(" ", "-")

@register.filter
def return_uppercase(l, i):
    try:
        return l[i].upper()
    except:
        return None

@register.filter
def make_lowercase(l):
    return l.lower()
