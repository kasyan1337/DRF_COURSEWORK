from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'telegram_chat_id')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['password'],
                                              validated_data['telegram_chat_id'])
        return user
