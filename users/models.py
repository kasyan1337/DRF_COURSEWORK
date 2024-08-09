from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)
    notification_time = models.TimeField(blank=True, null=True)