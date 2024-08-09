from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'action', 'time', 'place', 'is_pleasant', 'reward', 'duration']
        read_only_fields = ['user']