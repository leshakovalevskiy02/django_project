from django.urls import path
from users import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),    # users:login
    path("logout/", LogoutView.as_view(), name="logout"),  # users:logout
    path("registration/", views.RegistrationUser.as_view(), name="registration"),
    path("registration_done/", views.registration_done, name="registration_done")
]