from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Adres e-mail", required=True, error_messages={'unique': 'Ten adres e-mail jest już używany.'})
    first_name = forms.CharField(label="Imię", max_length=30)
    last_name = forms.CharField(label="Nazwisko", max_length=30)
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


class utworz_blogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')