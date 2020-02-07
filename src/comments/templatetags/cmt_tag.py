from django import template
from django.utils.dateparse import parse_datetime

register = template.Library()

@register.filter
def get_parent_class(value):
  return value['parent_content_type']['app_label']


@register.filter
def to_date(value):
  return parse_datetime(value)