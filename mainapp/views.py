from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.forms import UserCreationForm
from .models import User

def homepage(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, "register.html", { "form": form})

def login(request):
    return  render(request, "login.html")
