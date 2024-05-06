from django.contrib import admin
from django.urls import path
from . import views




urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('my_profile/', views.my_profile, name='my_profile'),
]
