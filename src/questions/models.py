from django.db import models

class Questions(models.Model):
    Create_Question = models.TextField(max_length=200)
    Elaborate_Question=models.TextField(max_length=500)
