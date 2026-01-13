from rest_framework import serializers


def validate_linked_habit_and_reward(habit):
    """1) Исключить одновременный выбор связанной привычки и вознаграждения."""
    if habit.linked_habit and habit.reward:
        raise serializers.ValidationError(
            "Нельзя одновременно указывать связанную привычку и вознаграждение."
        )


def validate_time_to_complete(habit):
    """2) Время выполнения не больше 120 секунд."""
    if habit.time_to_complete > 120:
        raise serializers.ValidationError(
            "Время выполнения не должно превышать 120 секунд (2 минуты)."
        )


def validate_linked_habit_is_pleasant(habit):
    """3) В связанные привычки могут попадать только приятные привычки."""
    if habit.linked_habit and not habit.linked_habit.is_pleasant:
        raise serializers.ValidationError(
            "Связанная привычка должна быть приятной привычкой."
        )


def validate_pleasant_habit_no_reward_or_linked(habit):
    """4) У приятной привычки не может быть вознаграждения или связанной привычки."""
    if habit.is_pleasant:
        if habit.reward:
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения."
            )
        if habit.linked_habit:
            raise serializers.ValidationError(
                "У приятной привычки не может быть связанной привычки."
            )


def validate_periodicity(habit):
    """5) Периодичность повторения от 1 до 7 дней включительно."""
    if habit.periodicity < 1 or habit.periodicity > 7:
        raise serializers.ValidationError(
            "Периодичность должна быть от 1 до 7 дней включительно."
        )


def validate_habit(habit):
    """Вызов всех проверок сразу."""
    validate_linked_habit_and_reward(habit)
    validate_time_to_complete(habit)
    validate_linked_habit_is_pleasant(habit)
    validate_pleasant_habit_no_reward_or_linked(habit)
    validate_periodicity(habit)
