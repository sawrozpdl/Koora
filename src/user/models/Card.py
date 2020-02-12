from django.db import models


class Card(models.Model):

    card_holder = models.CharField(max_length=250)
    card_number = models.CharField(max_length=16)
    exp_date = models.DateTimeField()
    cvc = models.IntegerField()

    def __str__(self):
        return str(self.card_holder)
