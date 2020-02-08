from django import template
from django.utils.dateparse import parse_datetime

register = template.Library()

@register.filter
def get_parent_class(value):
  return value['parent_content_type']['app_label']


@register.filter
def to_date(value):
  return parse_datetime(value)


@register.filter
def vote_type_for(value, user_id):
  votes = value['all_votes']
  for vote in votes:
      vote_type = vote['is_upvote'] if (vote['user'] == user_id) else -1
      if vote_type != -1:
          return vote_type
  return -1