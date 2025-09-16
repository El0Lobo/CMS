from django import template
register = template.Library()

@register.filter
def get(d, key):
    """Safe dict-get for templates: {{ obj|get:'key' }}"""
    try:
        return d.get(key, "")
    except AttributeError:
        return ""
