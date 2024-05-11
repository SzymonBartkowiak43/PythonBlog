from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog, Post, Comment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Adres e-mail", required=True, error_messages={'unique': 'Ten adres e-mail jest już używany.'})
    first_name = forms.CharField(label="Imię", max_length=30)
    last_name = forms.CharField(label="Nazwisko", max_length=30)
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


class BlogCreationForm(forms.ModelForm):
    is_private = forms.BooleanField(label="Czy blog ma być prywatny?", required=False)
    password = forms.CharField(label="Hasło dla bloga", max_length=128, required=False, widget=forms.PasswordInput)

    class Meta:
        model = Blog
        fields = ('title', 'description')

    def clean(self):
        cleaned_data = super().clean()
        is_private = cleaned_data.get('is_private')
        password = cleaned_data.get('password')

        if is_private and not password:
            raise forms.ValidationError("Jeśli chcesz, aby blog był prywatny, wprowadź hasło.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        is_private = self.cleaned_data.get('is_private')
        password = self.cleaned_data.get('password')

        if is_private:
            instance.is_private = True
            instance.password = password
        else:
            instance.is_private = False
            instance.password = None

        if commit:
            instance.save()
        return instance

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'visibility', 'password', 'image']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'author': forms.HiddenInput(), 'post': forms.HiddenInput()}
