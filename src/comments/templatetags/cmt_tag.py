from django import template
register = template.Library()

@register.filter
def get_parent_class(value):
  return value['parent_content_type']['app_label']