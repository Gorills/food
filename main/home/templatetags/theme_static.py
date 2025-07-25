from django import template
register = template.Library()
from setup.models import ThemeSettings
try:
    theme_address = 'fast_theme'
except:
    theme_address = 'fast_theme'

@register.simple_tag()
def get_static(file):
    
    return '/core/theme/'+theme_address+'/' + file


@register.simple_tag()
def get_libs(file):
    return '/core/libs/' + file 