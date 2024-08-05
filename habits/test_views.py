import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from habits.models import Habit

@pytest.mark.django_db
def test_habit_list():
    client = APIClient()
    user = User.objects.create_user(username='test_user', password='test_password')
    client.force_authenticate(user=user)
    Habit.objects.create(
        user=user,
        action='run',
        time='12:00:00',
        place='park',
        is_pleasant=False,
        frequency=1,
        duration=60,
        is_public=False
    )
    response = client.get('/api/habits/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['user'] == user.id
    assert response.data[0]['action'] == 'run'
    assert response.data[0]['time'] == '12:00:00'
    assert response.data[0]['place'] == 'park'
    assert response.data[0]['is_pleasant'] is False
    assert response.data[0]['frequency'] == 1
    assert response.data[0]['duration'] == 60
    assert response.data[0]['is_public'] is False
    assert 'id' in response.data[0]

