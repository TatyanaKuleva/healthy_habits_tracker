import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from tracker.models import Habit
from tracker.services import parse_habit_time, send_telegram_message

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Тестирование отправки напоминаний о привычках в Telegram без Celery"

    def add_arguments(self, parser):
        parser.add_argument(
            "--time",
            type=str,
            help="Время для проверки в формате HH:MM (например, 20:11). Если не указано, используется текущее время",
        )
        parser.add_argument(
            "--habit-id",
            type=int,
            help="ID конкретной привычки для отправки (необязательно)",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Отправить сообщения для всех привычек с указанным временем, даже если время не совпадает",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("=== Тестирование отправки напоминаний о привычках ===")
        )

        # Определяем время для проверки
        if options["time"]:
            try:
                test_time_obj = datetime.strptime(options["time"], "%H:%M").time()
                test_hour_minute = test_time_obj.strftime("%H:%M")
                self.stdout.write(f"Используется указанное время: {test_hour_minute}")
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(
                        f"Неверный формат времени: {options['time']}. Используйте формат HH:MM"
                    )
                )
                return
        else:
            # Используем текущее время
            now_utc = timezone.now()
            now_local = timezone.localtime(now_utc)
            test_time_obj = now_local.time()
            test_hour_minute = test_time_obj.strftime("%H:%M")
            self.stdout.write(f"Используется текущее время: {test_hour_minute}")
            self.stdout.write(f"UTC время: {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            self.stdout.write(
                f"Локальное время (Europe/Moscow): {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            )

        # Получаем привычки
        if options["habit_id"]:
            try:
                habits = [Habit.objects.get(id=options["habit_id"])]
                self.stdout.write(f"Найдена привычка с ID={options['habit_id']}")
            except Habit.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Привычка с ID={options['habit_id']} не найдена")
                )
                return
        else:
            habits = Habit.objects.all()
            self.stdout.write(f"Найдено привычек в базе: {habits.count()}")

        if not habits:
            self.stdout.write(self.style.WARNING("В базе нет привычек"))
            return

        # Обрабатываем привычки
        sent_count = 0
        skipped_count = 0
        error_count = 0

        for habit in habits:
            self.stdout.write("\n" + "-" * 60)
            self.stdout.write(f"Привычка ID={habit.id}")
            self.stdout.write(f"  Действие: {habit.action}")
            self.stdout.write(f"  Время: {habit.time}")
            self.stdout.write(f"  Место: {habit.place}")
            self.stdout.write(
                f"  Пользователь: {habit.creator.email} (ID={habit.creator.id})"
            )
            self.stdout.write(f"  Chat ID: {habit.creator.tg_chat_id}")

            habit_time_str = habit.time
            habit_time_obj = parse_habit_time(habit_time_str)
            if not habit_time_obj:
                self.stdout.write(
                    self.style.ERROR(
                        f"  ✗ Ошибка парсинга времени: '{habit_time_str}' (поддерживаются форматы HH:MM или HH:MM:SS)"
                    )
                )
                skipped_count += 1
                continue

            habit_hour_minute = habit_time_obj.strftime("%H:%M")

            # Проверяем совпадение времени (если не указан флаг --all)
            if not options["all"]:
                if habit_hour_minute != test_hour_minute:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  ⏭ Время не совпадает: {habit_hour_minute} != {test_hour_minute} (пропуск)"
                        )
                    )
                    skipped_count += 1
                    continue

            self.stdout.write(f"  ✓ Время совпадает: {habit_hour_minute}")

            # Проверяем наличие chat_id
            chat_id = habit.creator.tg_chat_id
            if not chat_id:
                self.stdout.write(
                    self.style.WARNING(
                        "  ✗ У пользователя отсутствует chat_id (пропуск)"
                    )
                )
                skipped_count += 1
                continue

            # Отправляем сообщение
            message = f"Напоминание: пора выполнять привычку '{habit.action}'!"
            self.stdout.write(f"Отправка сообщения в Telegram...")
            self.stdout.write(f"Chat ID: {chat_id}")
            self.stdout.write(f"Сообщение: {message}")

            try:
                send_telegram_message(chat_id, message)
                self.stdout.write(self.style.SUCCESS(f"Сообщение успешно отправлено!"))
                sent_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при отправке: {e}"))
                error_count += 1
                logger.error(
                    f"Ошибка при отправке сообщения для привычки ID={habit.id}: {e}",
                    exc_info=True,
                )

        # Итоговая статистика
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("=== Итоговая статистика ==="))
        self.stdout.write(f"Всего обработано привычек: {len(habits)}")
        self.stdout.write(self.style.SUCCESS(f"Успешно отправлено: {sent_count}"))
        self.stdout.write(self.style.WARNING(f"Пропущено: {skipped_count}"))
        self.stdout.write(self.style.ERROR(f"Ошибок: {error_count}"))
        self.stdout.write("=" * 60)
