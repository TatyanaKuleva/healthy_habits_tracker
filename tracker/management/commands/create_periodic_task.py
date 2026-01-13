from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Создает периодичечкую задачу по рассылки напоминаний"

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )
        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="Напоминание о назначенной привычке",
            task="tracker.tasks.send_habit_reminders",
        )
        self.stdout.write(self.style.SUCCESS("Periodic task created or already exists"))