from django import template
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter
def render_markdown(value):
    if not value:
        return ""
    html = markdown(value, extensions=["extra"])
    return mark_safe(html)
