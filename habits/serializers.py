from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "action",
            "time",
            "place",
            "is_pleasant",
            "reward",
            "duration",
            "is_public",
            "frequency",
            "related_habit",
            "notification_time",
        ]
        read_only_fields = ["user"]

    def validate(self, data):
        # Validate duration # Validator 1
        if data["duration"] > 120:
            raise serializers.ValidationError(
                "Duration must be less than or equal to 120 seconds."
            )

        # Validator for notification time for unpleasant habits Validator 2
        if not data["is_pleasant"]:
            # Check if notification_time is provided in the data
            notification_time_in_data = data.get("notification_time")
            user_notification_time = self.context[
                "request"].user.notification_time
            if not notification_time_in_data and not user_notification_time:
                raise serializers.ValidationError(
                    "Notification time must be set for unpleasant habits."
                )

        # related habut and reward not set validation # Validator 3
        if data.get("related_habit") and not data.get(
                "related_habit").is_pleasant:
            raise serializers.ValidationError(
                "Only pleasant habits can be related habits."
            )

        # pleasant habit cannot have a reward or a related habit # Validator 4
        if data["is_pleasant"] and (data.get("reward") or
                                    data.get("related_habit")):
            raise serializers.ValidationError(
                "A pleasant habit cannot have a reward or a related habit."
            )

        # validateor frequency # Validator 5
        if data["frequency"] < 1 or data["frequency"] > 7:
            raise serializers.ValidationError(
                "Frequency must be between 1 and 7 days.")

        return data
