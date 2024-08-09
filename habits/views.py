from rest_framework import viewsets, permissions

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Habit.objects.filter(user=self.request.user)  # shows only user's habits if user is authenticated
        return Habit.objects.filter(is_public=True)  # shows only public habits if user is not authenticated

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # saves with currently authenticated user
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)