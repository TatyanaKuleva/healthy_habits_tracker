from rest_framework import generics, permissions
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnlyPublic

class HabitListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(creator=user) | Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPublic]

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(creator=user) | Habit.objects.filter(is_public=True)