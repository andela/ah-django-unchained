from django.urls import path


from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ResetPasswordAPIView, UpdatePasswordAPIView, VerifyAPIView,
    ResendVerifyAPIView, SocialAuthenticationView
)

app_name = "authentication"
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="auth-register"),
    path('users/login/', LoginAPIView.as_view(), name="auth-login"),
    path('users/passwordreset/', ResetPasswordAPIView.as_view(), name="passwordreset"),
    path('users/passwordresetdone/<token>', UpdatePasswordAPIView.as_view(), name="passwordresetdone"),
    path('users/verify/<token>/', VerifyAPIView.as_view(), name="auth-verify"),
    path('users/resend-verification/', ResendVerifyAPIView.as_view(), name="auth-reverify"),
    path('login/oauth/', SocialAuthenticationView.as_view(), name="social_auth")
]
