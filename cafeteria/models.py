from django.db import models
from accounts.models import User
from django.utils import timezone


class Seat(models.Model):
    # static fields
    SEAT_TIME_CHOICE = (
        (1, 'first'),
        (2, 'second'),
    )
    half = models.IntegerField(choices=SEAT_TIME_CHOICE, blank=False)
    # dynamic fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}-({self.half})] {self.user.email}'
