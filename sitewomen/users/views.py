from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request, username=cleaned_data["username"],
                                         password=cleaned_data["password"])
            if user is not None and user.is_active:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "users/login.html", context=context)

def logout_user(request):
    logout(request)
    return redirect("users:login")
