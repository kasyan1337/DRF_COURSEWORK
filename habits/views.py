from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from habits.models import Habit
from habits.serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitPagination(PageNumberPagination):
    page_size = 5


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Habit.objects.all()


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
