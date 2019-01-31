import os
import jwt
from datetime import datetime, timedelta
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend, AuthAlreadyAssociated
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import IntegrityError
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from . import models
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ResetSerializerEmail, ResetSerializerPassword, SocialAuthSerializer
)
from .models import User
from .utils import send_link


class RegistrationAPIView(generics.CreateAPIView):

    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', None)
        payload = {'email':  email,
                    "iat": datetime.now(),
                    "exp": datetime.utcnow()
                    + timedelta(minutes=30)}
        token = jwt.encode(payload,
                            settings.SECRET_KEY,
                            algorithm='HS256').decode('utf-8')       
        template = 'email_verify_account.html'
        url = '/api/users/verify/'
        subject = "Authors Haven Verification Link"
        send_link(email,subject, template, url, token)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, token):
        try:
            email = jwt.decode(token, settings.SECRET_KEY)['email']
            user = User.objects.get(email=email)
            if user.is_verified:
                message = {
                    "message": "Your account is already verified.",
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            user.is_verified = True
            user.save()
            message = {
                "message": "Your account has been successfully verified.",
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception:
            message = {"errors": {
                "email": [
                    "Verification link is invalid."
                ]}
            }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY)
        email = payload['email']
        template = 'email_verify_account.html'
        url = '/api/users/verify/'
        subject = "Authors Haven Verification Link"
        send_link(email,subject, template, url, token)
        message = {
            "message": "Verification link sent successfully. Please check your email.",
        }
        return Response(message, status=status.HTTP_200_OK)


class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.CreateAPIView):
    """Sends password reset link to email"""
    serializer_class = ResetSerializerEmail

    def post(self, request):

        email = request.data['email']
        if email == "":
            return Response({"errors": {    
                "email": ["An email is required"]}})
        user = models.User.objects.filter(email=email)
        if user:
            token = jwt.encode({"email": email, "iat": datetime.now(),
                                "exp": datetime.utcnow() + timedelta(minutes=5)},
                               settings.SECRET_KEY, algorithm='HS256').decode()
            to_email = [email]
            DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
            host_url = os.getenv("PASSWORD_RESET_URL")
            link = 'http://' + str(host_url) + '/users/passwordresetdone/' + token
            message = render_to_string(
                'email_password_reset.html', {
                    'user': to_email,
                    'domain': link,
                    'token': token,
                    'username': to_email,
                    'link': link
                })
            send_mail('You requested password reset',
                      'Reset your password', 'DEFAULT_FROM_EMAIL',
                      [to_email, ], html_message=message, fail_silently=False)
            message = {
                "message": "Successfully sent.Check your email",
            }
            return Response(message, status=status.HTTP_200_OK)

        else:
            message = {"errors": {
                "email": [
                    "User with this email does not exist."
                ]}
            }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordAPIView(generics.UpdateAPIView):
    """Allows you to reset you password"""
    serializer_class = ResetSerializerPassword

    def put(self, request, token, **kwargs):
        try:
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if password != confirm_password:
                return Response({"Passwords do not match"},
                                status=status.HTTP_200_OK)
            serializer = self.serializer_class(data={"password": password,
                                                     "confirm_password": confirm_password})
            serializer.is_valid(raise_exception=True)
            decode_token = jwt.decode(token, settings.SECRET_KEY,
                                      algorithms='HS256')
            email = decode_token.get('email')
            user = models.User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return Response({"message": "Password Successfully Updated"},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"The link expired"},
                            status=status.HTTP_400_BAD_REQUEST)
                            

class SocialAuthenticationView(generics.CreateAPIView):
    """Social authentication."""
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer
    render_classes = (UserJSONRenderer,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = request.data['provider']
        strategy = load_strategy(request)
        authenticated_user = request.user if not request.user.is_anonymous else None

        try:
            backend = load_backend(
                strategy=strategy,
                name=provider,
                redirect_uri=None
            )

            if isinstance(backend, BaseOAuth1):
                if "access_token_secret" in request.data:
                    token = {
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret':
                        request.data['access_token_secret']
                    }
                else:
                    return Response({'error':
                                    'Please enter your secret token'},
                                    status=status.HTTP_400_BAD_REQUEST)
            elif isinstance(backend, BaseOAuth2):
                token = serializer.data.get('access_token')
        except MissingBackend:
            return Response({
                'error': 'Please enter a valid social provider'
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = backend.do_auth(token, user=authenticated_user)
        except (AuthAlreadyAssociated, IntegrityError):
            return Response({
                "errors": "You are already logged in with another account"},
                status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response({
                "errors": "Invalid token"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if user:
            user.is_active = True
            username = user.username
            email = user.email

        date = datetime.now() + timedelta(days=20)
        payload = {
            'email': email,
            'username': username,
            'exp': int(date.strftime('%s'))
        }
        user_token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm='HS256')
        serializer = UserSerializer(user)
        serialized_details = serializer.data
        serialized_details["token"] = user_token
        return Response(serialized_details, status.HTTP_200_OK)
