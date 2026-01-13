from datetime import datetime

from celery import shared_task
from django.utils.timezone import now

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    current_time = now().time()
    current_hour_minute = current_time.strftime("%H:%M")

    habits = Habit.objects.all()

    for habit in habits:
        habit_time_str = habit.time

        try:
            habit_time_obj = datetime.strptime(habit_time_str, "%H:%M").time()
        except (ValueError, TypeError):
            continue

        habit_hour_minute = habit_time_obj.strftime("%H:%M")

        if habit_hour_minute == current_hour_minute:
            chat_id = habit.creator.chat_id
            print(chat_id, habit_hour_minute)
            if not chat_id:
                continue

            message = f"Напоминание: пора выполнять привычку '{habit.action}'!"
            send_telegram_message(chat_id, message)
