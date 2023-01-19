from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('change_password/', UserChangePassword.as_view()),
    path('send_reset_password_email/', SendPasswordResetEmailView.as_view()),
    path('user_reset_password/<uid>/<token>/', UserPasswordResetView.as_view()),
]