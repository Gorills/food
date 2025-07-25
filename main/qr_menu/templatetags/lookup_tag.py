from django import template

register = template.Library()

@register.filter
def lookup(categories, field):
    return any(getattr(category, field) for category in categories.keys())