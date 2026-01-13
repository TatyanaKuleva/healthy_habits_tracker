from django.urls import path
from tracker.apps import TrackerConfig
from .views import HabitCreateAPIView, HabitListAPIView, PublicHabitListAPIView,  HabitRetrieveUpdateDestroyAPIView

app_name = TrackerConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit-list'),
    path('habits/public/', PublicHabitListAPIView.as_view(), name='habit-public-list'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('habits/<int:pk>/', HabitRetrieveUpdateDestroyAPIView.as_view(), name='habit-detail')
]