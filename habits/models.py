from django.contrib.auth.models import User
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def save(self, *args, **kwargs):
        if self.related_habit and self.reward:
            raise ValueError('A habit cannot have a related habit and a reward at the same time.')
        if self.duration > 120:
            raise ValueError('Duration must be less than or equal to 120 seconds.')
        super.save(*args, **kwargs)  # Calls the parent class's save method to save the instance to the database
