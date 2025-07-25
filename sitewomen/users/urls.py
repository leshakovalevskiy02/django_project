from django.urls import path, reverse_lazy
from users import views
from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView, PasswordResetDoneView,
                                       PasswordResetCompleteView)


app_name = 'users'

urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),    # users:login
    path("logout/", LogoutView.as_view(), name="logout"),  # users:logout

    path("registration/", views.RegistrationUser.as_view(), name="registration"),
    path("registration/confirm_email/", views.confirm_email, name="confirm_email"),
    path("registration/verify_email/<uuid:token>/", views.verify_email, name="verify_email"),
    path("registration_done/", views.registration_done, name="registration_done"),

    path("profile/", views.UserProfile.as_view(), name="profile"),
    path("password_change/", views.UserPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
                                  name="password_change_done"),

    path("password_reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
                                  name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(),
                                  name="password_reset_confirm"),
    path("password_reset/complete/", PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
                                  name="password_reset_complete")
]