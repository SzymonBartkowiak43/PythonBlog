from django.shortcuts import render
from django.http import *


def homepage(request):
    return render(request, "home.html")
