from django.db import models


class Social(models.Model):

    reddit_username = models.CharField(max_length=250, null=True)
    facebook_username = models.CharField(max_length=250, null=True)
    linkedin_username = models.CharField(max_length=250, null=True)
    discord_username = models.CharField(max_length=250, null=True)
    github_username = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.reddit_username)
