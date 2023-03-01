from rest_framework import serializers
from loguru import logger

from back_edesoft.models import *


class NotAuthorizedSerializer(serializers.Serializer):
    """Status 401 Response."""

    detail = serializers.CharField(default="Not authorized")


class AuthenticationFailedSerializer(serializers.Serializer):
    """Status 403 Response."""

    detail = serializers.CharField(default="Authorization header not found")


class GatewayTimeoutSerializer(serializers.Serializer):
    """Status 504 Response."""

    detail = serializers.CharField(default="Gateway Timeout")


class UserSerializer(serializers.ModelSerializer):
    """User Serializer."""

    class Meta:
        model = User
        fields = "__all__"

class TaskSerializer(serializers.Serializer):
    """Task Serializer."""

    bucket_name = serializers.CharField()
    object_key = serializers.CharField()
