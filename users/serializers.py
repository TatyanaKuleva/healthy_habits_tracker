from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "phone_number",
            "avatar",
            "city",
            "tg_chat_id",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password", "phone_number", "avatar", "city"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number"),
            avatar=validated_data.get("avatar"),
            city=validated_data.get("city"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
