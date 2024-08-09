from django.shortcuts import render
from rest_framework import generics

from users.models import CustomUser
from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer