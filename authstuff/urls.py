from django.urls import path, re_path

from dj_rest_auth.views import (LoginView, LogoutView, PasswordChangeView,
                                PasswordResetConfirmView, PasswordResetView)
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView

from .views import UserDetailsView, CSRFView, UserDeleteView

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # URLs that do not require a session or valid token
    path('csrf', CSRFView.as_view(), name='csrf'),
    path('password/reset', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('login', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout', LogoutView.as_view(), name='rest_logout'),
    path('user', UserDetailsView.as_view(), name='rest_user_details'),
    path('user/delete', UserDeleteView.as_view(), name='rest_user_delete'),
    path('password/change', PasswordChangeView.as_view(), name='rest_password_change'),
    # Register views
    path('register', RegisterView.as_view(), name='rest_register'),
    path('verify-email', VerifyEmailView.as_view(), name='rest_verify_email'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
