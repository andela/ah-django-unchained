from django.urls import path


from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    ResetPasswordAPIView, UpdatePasswordAPIView
)

app_name = "authentication"
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view(), name="auth-register"),
    path('users/login/', LoginAPIView.as_view(), name="auth-login"),
    path('users/passwordreset/', ResetPasswordAPIView.as_view(), name="passwordreset"),
    path('users/passwordresetdone/<token>', UpdatePasswordAPIView.as_view(), name="passwordresetdone"),


]
