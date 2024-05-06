from django.shortcuts import render
from django.http import *


def homepage(request):
    return render(request, "home.html")

def register(request):
    return render(request, "register.html")

def login(request):
    return  render(request, "login.html")
