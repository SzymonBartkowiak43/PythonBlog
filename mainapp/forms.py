from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog, Post, Comment, Tag, PostTag


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="e-mail", required=True, error_messages={'unique': 'This email is already in use'})
    first_name = forms.CharField(label="name", max_length=30)
    last_name = forms.CharField(label="surname", max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')


class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')


class PostCreationForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    new_tags = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add new tags separated by commas'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags', 'new_tags', 'is_private', 'password']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tags = self.cleaned_data['tags']
            new_tags = self.cleaned_data['new_tags']

            for tag in tags:
                PostTag.objects.create(post=instance, tag=tag)

            if new_tags:
                new_tag_names = [tag.strip() for tag in new_tags.split(',')]
                for name in new_tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    PostTag.objects.create(post=instance, tag=tag)
            self.save_m2m()
        return instance


class PostEditForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    new_tags = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add new tags separated by commas'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags', 'new_tags', 'is_private', 'password']

    def save(self, commit=True):
        instance = super().save(commit=False)
        tags = self.cleaned_data['tags']
        new_tags = self.cleaned_data['new_tags']

        if commit:
            instance.save()
            PostTag.objects.filter(post=instance).delete()
            for tag in tags:
                PostTag.objects.create(post=instance, tag=tag)

            if new_tags:
                new_tag_names = [tag.strip() for tag in new_tags.split(',')]
                for name in new_tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    PostTag.objects.create(post=instance, tag=tag)
            self.save_m2m()
        return instance


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Dodaj komentarz'})
        }


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
