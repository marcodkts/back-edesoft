from django.contrib.auth.models import User as DjangoUser
from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from loguru import logger
from rest_framework import authentication, exceptions

from core import settings


class SecretsTokenAuthentication(authentication.TokenAuthentication):
    """Secrets Token Authentication Class."""

    logger.debug("SecretsTokenAuthentication Loaded")
    def authenticate(self, request):
        key = request.META.get("HTTP_AUTHORIZATION")
        """Authenticate Credentials."""
        if key != settings.SECRET_TOKEN:
            raise exceptions.AuthenticationFailed(_("Authorization header not found"))

        user, created = DjangoUser.objects.get_or_create(email="tech@wolfgear.tech")
        if created:
            user.is_staff = True
            user.username = "API User"
            user.save()

        return user, key

class SecretsTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    """Secrets Token Authentication Scheme."""

    target_class = "core.tools.auth.SecretsTokenAuthentication"
    name = "Token Authorization"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
