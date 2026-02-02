from django import template
register = template.Library()
from setup.models import ThemeSettings

# Список тем, для которых есть папка в core/theme/
VALID_THEMES = ('default', 'china', 'sushi', 'fast_theme', 'flowers_light')

@register.simple_tag()
def get_static(file):
    try:
        theme_address = ThemeSettings.objects.get().name
        if theme_address not in VALID_THEMES:
            theme_address = 'fast_theme'
    except Exception:
        theme_address = 'fast_theme'
    return '/core/theme/' + theme_address + '/' + file


@register.simple_tag()
def get_libs(file):
    return '/core/libs/' + file 