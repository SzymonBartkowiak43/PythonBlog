from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import *

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from .forms import CustomUserCreationForm, utworz_blogForm


def homepage(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return redirect('login')
    else:
        return render(request, "login.html")


def utworz_blog_widok(request):
    if request.method == "POST":
        form = utworz_blogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user.get()
            blog.save()
            return redirect('homepage')
    else:
        form = utworz_blogForm()
    return render(request, "utworz_blog.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('homepage')
