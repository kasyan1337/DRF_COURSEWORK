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

    def clean(self):
        print(f'Cleaning habit: {self.action}')
        if not self.user.is_superuser:
            if self.related_habit and self.reward:
                raise ValidationError('A habit cannot have a related habit and a reward at the same time.')
            if self.duration > 120:
                raise ValidationError('Duration must be less than or equal to 120 seconds.')
            if not self.is_pleasant and not self.user.notification_time:
                raise ValidationError('Notification time must be set for unpleasant habits.')

    def save(self, *args, **kwargs):
        self.clean()  # Calls the clean method to validate the instance
        super(Habit, self).save(*args,
                                **kwargs)  # Calls the parent class's save method to save the instance to the database
