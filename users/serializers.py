from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from users.models import UserConfirmation


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfirmation
        fields = ['code']
