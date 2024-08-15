from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(
        _("email address"), unique=True
    )
    # No idea why this is needed, we are doing API for telegram

    telegram_chat_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    notification_time = models.TimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # ❌ Также не внесены обычные настройки модели (Meta)
    # OK
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["id"]
