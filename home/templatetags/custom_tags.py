from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def versioned_static(path):
    return f"{settings.STATIC_URL}{path}?v={settings.STATIC_VERSION}"