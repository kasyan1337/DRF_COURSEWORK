import pytest
from django.contrib.auth.models import User

from habits.models import Habit


@pytest.mark.django_db
def test_create_habit():
    user = User.objects.create_user(username='test_user', password='test_password')
    habit = Habit.objects.create(
        user=user,
        action='run',
        time='12:00',
        place='park',
        is_pleasant=True,
        frequency=3,
        duration=60,
        is_public=True
    )

    assert habit.user == user
    assert habit.user.username == 'test_user'
    assert habit.action == 'run'
    assert habit.time == '12:00'
    assert habit.place == 'park'
    assert habit.is_pleasant is True
    assert habit.frequency == 3
    assert habit.duration == 60
    assert habit.is_public is True

