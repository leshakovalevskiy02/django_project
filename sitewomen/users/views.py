from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginForm, RegistrationForm


class LoginUser(LoginView):
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}
    form_class = LoginForm
    redirect_authenticated_user = True


class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = "users/registration.html"
    extra_context = {
        "title": "Регистрация"
    }
    success_url = reverse_lazy("users:registration_done")


def registration_done(request):
    return render(request, "users/registration_done.html")
