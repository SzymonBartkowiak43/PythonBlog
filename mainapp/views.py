from django.shortcuts import render
from django.http import *


def homepage(request):
    return render(request, "home.html")

def my_profile(request):
    return render(request,"my_profile.html")
