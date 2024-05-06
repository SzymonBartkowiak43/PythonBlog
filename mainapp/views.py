from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login(request, form.get_user())
            # if 'next' in request.POST:
            #     return redirect(request.POST.get('next'))
            # else:
            return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", { "form": form })

# def logout_view(request):
#     if request.method == "POST":
#         logout(request)
#         return redirect("posts:list")


