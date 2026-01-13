from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Через день'),
        (3, '1 раз в три дня'),
        (4, '1 раз в четыре дня'),
        (5, '1 раз в пять дней'),
        (6, '1 раз в шесть дней'),
        (7, '1 раз в семь дней')
    ]

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255, help_text='Действие — привычка в одном предложении')
    time = models.CharField(max_length=50, help_text='Время выполнения привычки')
    place = models.CharField(max_length=100, help_text='Место выполнения привычки')
    is_pleasant = models.BooleanField(default=False, help_text='Приятная привычка, признак приятной привычки')
    linked_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pleasant_habits',
        help_text='Связанная приятная привычка, связана с полезной привычкой'
    )
    periodicity = models.PositiveIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        help_text='Периодичность выполнения (в днях)'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Вознаграждение после выполнения'
    )
    time_to_complete = models.PositiveIntegerField(
        default=120,
        help_text='Время на выполнение привычки в секундах'
    )
    is_public = models.BooleanField(default=False, help_text='Привычка доступна публично')


    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
