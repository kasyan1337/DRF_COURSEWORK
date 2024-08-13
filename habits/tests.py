from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit
from datetime import time

User = get_user_model()

class HabitAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.user.notification_time = time(8, 0)
        self.user.save()

        self.other_user = User.objects.create_user(username='otheruser', email='otheruser@example.com', password='otherpass')
        self.other_user.notification_time = time(8, 0)
        self.other_user.save()

        self.habit = Habit.objects.create(
            user=self.user,
            action='Morning Run',
            time='07:00',
            place='Park',
            is_pleasant=False,
            reward='Coffee',
            duration=20
        )

        self.other_habit = Habit.objects.create(
            user=self.other_user,
            action='Evening Walk',
            time='18:00',
            place='Garden',
            is_pleasant=True,
            reward='Tea',
            duration=15
        )

        self.list_url = reverse('habit-list-create')
        self.detail_url = reverse('habit-detail', kwargs={'pk': self.habit.pk})
        self.other_habit_detail_url = reverse('habit-detail', kwargs={'pk': self.other_habit.pk})
        self.client.login(username='testuser', password='testpass')

    def test_list_habits_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_habits = Habit.objects.filter(user=self.user)
        self.assertEqual(len(response.data['results']), user_habits.count())

    def test_list_habits_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'action': 'Evening Walk',
            'time': '18:00',
            'place': 'Park',
            'is_pleasant': True,
            'reward': 'Ice Cream',
            'duration': 30,
            'frequency': 1
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_habit_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            'action': 'Evening Walk',
            'time': '18:00',
            'place': 'Park',
            'is_pleasant': True,
            'reward': 'Ice Cream',
            'duration': 30,
            'frequency': 1
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_habit_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_habit_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_habit_authenticated(self):
        self.client.force_authenticate(user=self.user)
        self.user.notification_time = time(7, 0)
        self.user.save()

        data = {
            'action': 'Morning Run Updated',
            'time': '07:30',
            'place': 'Park',
            'is_pleasant': False,
            'reward': 'Coffee',
            'duration': 25,
            'frequency': 1,
            'notification_time': '07:00'
        }

        response = self.client.put(self.detail_url, data, format='json')
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_users_habit(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'action': 'Morning Run Updated',
            'time': '07:30',
            'place': 'Park',
            'is_pleasant': False,
            'reward': 'Coffee',
            'duration': 25
        }
        other_habit_exists = Habit.objects.filter(pk=self.other_habit.pk, user=self.other_user).exists()
        self.assertTrue(other_habit_exists)

        response = self.client.put(self.other_habit_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_habit_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_habit_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_other_users_habit(self):
        self.client.force_authenticate(user=self.user)
        other_habit_exists = Habit.objects.filter(pk=self.other_habit.pk, user=self.other_user).exists()
        self.assertTrue(other_habit_exists)

        response = self.client.delete(self.other_habit_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)