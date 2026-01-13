from django.urls import path
from tracker.apps import TrackerConfig
from .views import HabitListCreateAPIView, HabitRetrieveUpdateDestroyAPIView

app_name = TrackerConfig.name

urlpatterns = [
    path('habits/', HabitListCreateAPIView.as_view(), name='habit-list-create'),
    path('habits/<int:pk>/', HabitRetrieveUpdateDestroyAPIView.as_view(), name='habit-detail'),
]