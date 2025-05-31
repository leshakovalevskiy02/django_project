from django.contrib.auth.views import (LoginView, PasswordChangeView, PasswordResetView,
                                       PasswordResetConfirmView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import LoginForm, RegistrationForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth import get_user_model

from .models import Profile


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

    def form_valid(self, form):
        user = form.save()
        if user:
            Profile.objects.create(user=user)
        return super().form_valid(form)


def registration_done(request):
    return render(request, "users/registration_done.html")


class UserProfile(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {
        "title": "Профиль пользователя"
    }
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        cd = form.cleaned_data
        user = self.object.user
        user.first_name = cd["first_name"]
        user.last_name = cd["last_name"]
        user.save()
        return super().form_valid(form)

class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:password_change_done")
    form_class = UserPasswordChangeForm


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")