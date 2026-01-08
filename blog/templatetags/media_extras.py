from django import template
from django.core.files.storage import default_storage
from django.templatetags.static import static

register = template.Library()


@register.filter
def image_or_placeholder(image_field, placeholder_path="images/placeholder.svg"):
    if not image_field:
        return static(placeholder_path)
    try:
        if default_storage.exists(image_field.name):
            return image_field.url
    except Exception:
        return static(placeholder_path)
    return static(placeholder_path)


@register.filter
def path_or_placeholder(path, placeholder_path="images/placeholder.svg"):
    if not path:
        return static(placeholder_path)
    try:
        if default_storage.exists(path):
            return default_storage.url(path)
    except Exception:
        return static(placeholder_path)
    return static(placeholder_path)
