from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    auto_response_enabled = serializers.BooleanField(default=False)
    auto_response_delay = serializers.IntegerField(default=5, min_value=0)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "password_confirm",
            "email",
            "first_name",
            "last_name",
            "auto_response_enabled",
            "auto_response_delay",
        )
        extra_kwargs = {"email": {"required": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
