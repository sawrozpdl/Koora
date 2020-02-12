from django.db import models


class Social(models.Model):

    reddit_username = models.CharField(max_length=250, blank=True, default='')
    facebook_username = models.CharField(max_length=250, blank=True, default='')
    linkedin_username = models.CharField(max_length=250, blank=True, default='')
    discord_username = models.CharField(max_length=250, blank=True, default='')
    github_username = models.CharField(max_length=250, blank=True, default='')

    def __str__(self):
        return str(self.reddit_username)
