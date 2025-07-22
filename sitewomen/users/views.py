from django.contrib.auth import get_user_model
from django.contrib.auth.views import (LoginView, PasswordChangeView, PasswordResetView,
                                       PasswordResetConfirmView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from sitewomen import settings
from .forms import (LoginForm, RegistrationForm, ProfileUserForm, UserPasswordChangeForm, CustomPasswordResetForm,
                    CustomSetPasswordForm)
import uuid


def send_mail_to_email(request, user):
    token = uuid.uuid4()
    user.verification_token = token
    user.save()
    verification_link = request.build_absolute_uri(
        reverse('users:verify_email', args=[token]))
    send_mail(
        'Подтвердите ваш email',
        f'Для подтверждения email перейдите по ссылке: {verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True
    )

class LoginUser(LoginView):
    template_name = "users/login.html"
    extra_context = {"title": "Авторизация"}
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.email_verified:
            send_mail_to_email(self.request, user)
            return redirect("users:confirm_email")

        remember_me = form.cleaned_data["remember_me"]
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super().form_valid(form)


class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = "users/registration.html"
    extra_context = {
        "title": "Регистрация"
    }
    success_url = reverse_lazy("users:confirm_email")

    def form_valid(self, form):
        get_user_model().objects.filter(email=form.cleaned_data["email"]).delete()
        user = form.save(commit=False)
        send_mail_to_email(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)


def verify_email(request, token):
    user = get_object_or_404(get_user_model(), verification_token=token)
    user.email_verified = True
    user.save()
    return redirect("users:registration_done")


def confirm_email(request):
    return render(request, "users/confirm_email.html")


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

    def form_valid(self, form):
        messages.success(self.request, message="Пароль был успешно изменен")
        return super().form_valid(form)


class UserPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = CustomPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        user = form.save()
        user.email_verified = True
        return super().form_valid(form)