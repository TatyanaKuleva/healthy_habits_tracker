from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Habit
from .validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.email")

    class Meta:
        model = Habit
        fields = [
            "id",
            "creator",
            "action",
            "time",
            "place",
            "is_pleasant",
            "linked_habit",
            "periodicity",
            "reward",
            "time_to_complete",
            "is_public",
        ]

    def validate(self, data):
        habit_instance = Habit(**data)

        try:
            validate_habit(habit_instance)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        except serializers.ValidationError as e:
            raise e

        return data
