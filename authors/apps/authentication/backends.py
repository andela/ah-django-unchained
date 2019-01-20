import jwt

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
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string contains invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """Check that the user associated with the token
        exists in our database"""
        payload = jwt.decode(token, settings.SECRET_KEY)
        email = payload['email']
        try:
            user = User.objects.get(
                email=email,
                is_active=True
            )
            if not user:
                msg = "User does not exist"
                raise exceptions.AuthenticationFailed(msg)
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse(
                {'Error': "Token is invalid"},
                status=status.HTTP_403_FORBIDDEN)

        return user, token
        