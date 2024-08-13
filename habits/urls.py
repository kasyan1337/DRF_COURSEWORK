from django.urls import path
from .views import HabitListCreateView, HabitRetrieveUpdateDestroyView

urlpatterns = [
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-detail'),
]