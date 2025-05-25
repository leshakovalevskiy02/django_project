from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import LoginForm


class LoginUser(LoginView):
    template_name = "users/login.html"
    # next_page = reverse_lazy("home")
    extra_context = {"title": "Авторизация"}
    form_class = LoginForm
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse('home')


# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = authenticate(request, username=cleaned_data["username"],
#                                          password=cleaned_data["password"])
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return redirect("home")
#     else:
#         form = LoginForm()
#     context = {
#         "form": form
#     }
#     return render(request, "users/login.html", context=context)

# def logout_user(request):
#     logout(request)
#     return redirect("users:login")


# class LogoutUser(LogoutView):
#     next_page = reverse_lazy("users:login")