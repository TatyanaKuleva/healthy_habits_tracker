import logging

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import parse_habit_time, send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminders():
    # Используем localtime для получения времени в часовом поясе Django (Europe/Moscow)
    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)
    current_time = now_local.time()
    current_hour_minute = current_time.strftime("%H:%M")

    logger.info(f"=== Запуск задачи send_habit_reminders ===")
    logger.info(f"UTC время: {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info(
        f"Локальное время (Europe/Moscow): {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    logger.info(f"Текущее время для сравнения: {current_hour_minute}")

    habits = Habit.objects.all()
    logger.info(f"Найдено привычек в базе: {habits.count()}")

    for habit in habits:
        habit_time_str = habit.time
        logger.debug(
            f"Обработка привычки ID={habit.id}, action='{habit.action}', time='{habit_time_str}'"
        )

        habit_time_obj = parse_habit_time(habit_time_str)
        if not habit_time_obj:
            logger.warning(
                f"Ошибка парсинга времени для привычки ID={habit.id}, time='{habit_time_str}'"
            )
            continue

        habit_hour_minute = habit_time_obj.strftime("%H:%M")
        logger.debug(f"Привычка ID={habit.id}: время парсится как {habit_hour_minute}")

        logger.debug(
            f"Сравнение: habit_time='{habit_hour_minute}' vs current_time='{current_hour_minute}'"
        )

        if habit_hour_minute == current_hour_minute:
            logger.info(
                f"✓ ВРЕМЯ СОВПАЛО! Привычка ID={habit.id}, action='{habit.action}', time={habit_hour_minute}"
            )
            chat_id = habit.creator.chat_id
            logger.info(f"Chat ID пользователя: {chat_id}")

            if not chat_id:
                logger.warning(
                    f"У пользователя ID={habit.creator.id} отсутствует chat_id, пропускаем отправку"
                )
                continue

            message = f"Напоминание: пора выполнять привычку '{habit.action}'!"
            logger.info(
                f"Отправка сообщения в Telegram: chat_id={chat_id}, message='{message}'"
            )

            try:
                send_telegram_message(chat_id, message)
                logger.info(
                    f"✓ Сообщение успешно отправлено в Telegram для привычки ID={habit.id}"
                )
            except Exception as e:
                logger.error(
                    f"✗ Ошибка при отправке сообщения в Telegram для привычки ID={habit.id}: {e}",
                    exc_info=True,
                )
        else:
            logger.debug(
                f"Время не совпало для привычки ID={habit.id}: {habit_hour_minute} != {current_hour_minute}"
            )

    logger.info(f"=== Завершение задачи send_habit_reminders ===")
