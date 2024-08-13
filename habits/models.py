from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    time = models.TimeField()
    place = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                      related_name='related_habits')
    frequency = models.PositiveIntegerField(default=1)  # number of days
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()  # in seconds
    is_public = models.BooleanField(default=False)
    notification_time = models.TimeField(null=True, blank=True)