from datetime import timedelta

import requests
from celery import shared_task
from django.utils import timezone

from habit_tracker import settings
from habits.models import Habit


@shared_task
def send_remainders():
    now = timezone.now()
    habits = Habit.objects.filter(
        time__lte=now.time(), frequency__gte=(now - timedelta(days=1)).days()
    )
    for habit in habits:
        send_telegram_message(
            habit.user.telegram_chat_id,
            f"я буду {habit.action} в {habit.time} в {habit.place}",
        )


def send_telegram_message(chat_id, text):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)
