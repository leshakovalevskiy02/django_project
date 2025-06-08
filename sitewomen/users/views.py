from django.contrib.auth.views import (LoginView, PasswordChangeView, PasswordResetView,
                                       PasswordResetConfirmView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from sitewomen import settings
from .forms import LoginForm, RegistrationForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth.models import Permission


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
        perm = Permission.objects.get(codename="change_psw_perm")
        user.user_permissions.add(perm)
        return super().form_valid(form)

def registration_done(request):
    return render(request, "users/registration_done.html")


class UserProfile(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {
        "title": "Профиль пользователя",
        "default_image": settings.DEFAULT_USER_IMAGE
    }
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChangeView(PermissionRequiredMixin, PasswordChangeView):
    permission_required = "users.change_psw_perm"
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