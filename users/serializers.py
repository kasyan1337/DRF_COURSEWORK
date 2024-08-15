from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password", "telegram_chat_id", "email")

    # 	❌ При регистрации не обрабатывается пароль методом хэширования
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            telegram_chat_id=validated_data.get("telegram_chat_id"),
        )
        user.set_password(
            validated_data["password"]
        )  # set_password ensures that the password
        # is hashed correctly before saving it.
        user.save()
        return user
