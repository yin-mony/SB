from django.urls import path

from .views import (
    AvatarUploadView,
    CaptchaView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("captcha/", CaptchaView.as_view()),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("avatar/", AvatarUploadView.as_view()),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view()),
]

