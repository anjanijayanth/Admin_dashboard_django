from django import template

register = template.Library()  # Get the template library

@register.filter( name='status')
def to_uppercase(status_str, status_val):
    return status_str[int(status_val)][1]
