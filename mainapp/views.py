from django.shortcuts import render
from django.http import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def homepage(request):
    return render(request, "home.html")

def register(request):
    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        return credits("login")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", { "form": form })


