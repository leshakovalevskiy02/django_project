from django.urls import path, reverse_lazy
from users import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from .forms import UserPasswordChangeForm

app_name = 'users'

urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),    # users:login
    path("logout/", LogoutView.as_view(), name="logout"),  # users:logout
    path("registration/", views.RegistrationUser.as_view(), name="registration"),
    path("registration_done/", views.registration_done, name="registration_done"),
    path("profile/", views.UserProfile.as_view(), name="profile"),
    path("password_change/", PasswordChangeView.as_view(
                                template_name="users/password_change.html",
                                success_url=reverse_lazy("users:password_change_done"),
                                form_class=UserPasswordChangeForm),
                                name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(
                                template_name="users/password_change_done.html",
    ), name="password_change_done")
]