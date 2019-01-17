
import jwt
import os
from jwt import ExpiredSignatureError
from datetime import datetime, timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import BrowsableAPIRenderer

from authors.apps.authentication.backends import JWTAuthentication
from .renderers import UserJSONRenderer
from . import serializers
from . import models
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, 
    ResetSerializerEmail, ResetSerializerPassword
)


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
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

        username = request.data
        email = username['email']
        if email == "":
            return Response({"errors": {
                "email": ["An email is required"]}})
        user = models.User.objects.filter(email=email)
        if user:
            token = jwt.encode({"email": email, "iat": datetime.now(),
                                "exp": datetime.utcnow() + timedelta(minutes=5)},
                               settings.SECRET_KEY, algorithm='HS256').decode()
            to_email = [email]
            subject = "You requested a password Reset"
            DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
            host_url = os.getenv("PASSWORD_RESET_URL")
            link = 'http://' + str(host_url) + '/users/passwordresetdone/'+ token
            message = render_to_string(
                'email.html', {
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
                "Message": "Successfully sent.Check your email",
            }
            return Response(message, status=status.HTTP_200_OK)

        else:
            message = {"errors": {
                "email": [
                    "User with this email doesnot exist."
                ]}
            }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordAPIView(generics.UpdateAPIView):
    """Allows you to reset you password"""
    permission_classes = (AllowAny,)
    serializer_class = ResetSerializerPassword

    def put(self, request, token, **kwargs):
        try:
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if password != confirm_password:
                return Response({"Passwords do not match"},
                                status=status.HTTP_200_OK)
            serializer = self.serializer_class(data={"password": password,
                                                     "confirm_password":
                                                     confirm_password})
            serializer.is_valid(raise_exception=True)
            decode_token = jwt.decode(token, settings.SECRET_KEY,
                                      algorithms='HS256')
            email = decode_token.get('email')
            user = models.User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return Response({"Message": "Password Successfully Updated"},
                            status=status.HTTP_200_OK)
        except ExpiredSignatureError:
            return Response({"The link expired"},
                            status=status.HTTP_400_BAD_REQUEST)
