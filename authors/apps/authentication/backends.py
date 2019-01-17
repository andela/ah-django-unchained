import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponse
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework import status, exceptions

from .models import User


class JWTAuthentication(BaseAuthentication):
    """This validates jwt token"""

    def authenticate(self, request):
        """Checks the token and verify its valid"""
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) != 2:
            msg = 'Token header is invalid.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            payload = jwt.decode(
                auth, settings.SECRET_KEY, algorithm='HS256')
        except:
            raise AuthenticationFailed("Your token is invalid. ")

        try:
            user = User.objects.get(email=payload["email"])
        except User.DoesNotExist:
            raise AuthenticationFailed('no available user')

        if not user.is_active:
            raise AuthenticationFailed("Acount is not active.")
        return (user, auth)

    def generate_token(email, username):
        """Generate token."""
        date = datetime.now() + timedelta(days=20)
        payload = {
            'email': email,
            'username': username,
            'exp': int(date.strftime('%s'))
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()
