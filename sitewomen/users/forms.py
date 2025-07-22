from datetime import datetime
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или E-mail", widget=forms.TextInput(attrs={"class": "form-control w-25"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control w-25"}))
    remember_me = forms.BooleanField(label="Запомнить меня", required=False,
                        widget=forms.CheckboxInput(attrs={"class": "form-check-input px-0 mt-2"}))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control w-25'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control w-25'}))

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name"]
        labels = {
            'username': 'Логин',
            "email": "E-mail"
        }
        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control w-25'}),
            "email": forms.EmailInput(attrs={"class": "form-control w-25"}),
            "first_name": forms.TextInput(attrs={'class': 'form-control w-25'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control w-25'})
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.filter(email=email, email_verified=True).exists():
            reset_url = reverse_lazy('users:password_reset')
            raise ValidationError(mark_safe(f"""E-mail адрес {email} уже был использован для создания учетной 
            записи. Если эта учетная запись принадлежит вам, но вы забыли от неё пароль, то 
            <a href='{reset_url}'>попробуйте его восстановить</a>."""))

        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={"class": "form-control w-25"}))
    email = forms.CharField(disabled=True, required=False, label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control w-25"}))
    this_year = datetime.today().year
    date_birth = forms.DateField(label="Дата рождения",
            widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5)), attrs={"class": "form-select"}))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'date_birth', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control w-25"}),
            'last_name': forms.TextInput(attrs={"class": "form-control w-25"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control w-50"}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль",
                                   widget=forms.PasswordInput(attrs={"class": "form-control w-25"}))
    new_password1 = forms.CharField(label="Новый пароль",
                                    widget=forms.PasswordInput(attrs={"class": "form-control w-25"}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={"class": "form-control w-25"}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Адрес электронной почты",widget=forms.EmailInput(
                        attrs={"autocomplete": "email", "class": "form-control w-25"}))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Новый пароль", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control w-25"}))
    new_password2 = forms.CharField(label="Подтверждение нового пароля", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control w-25"}))