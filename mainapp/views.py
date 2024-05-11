from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import *

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Blog
from .forms import CustomUserCreationForm, BlogCreationForm, PostCreationForm, CommentCreationForm
from django.contrib.auth.decorators import login_required


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

def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blogi.html', {'blogs': blogs})

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

@login_required
def BlogCreationView(request):
    if request.method == "POST":
        form = BlogCreationForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user
            blog.save()
            return redirect('homepage')
    else:
        form = BlogCreationForm()
    return render(request, "utworz_blog.html", {"form": form})


def blog_details(request, pk):
    # Pobranie bloga z bazy danych na podstawie jego id
    blog = get_object_or_404(Blog, pk=pk)


    if blog.is_private:
        if request.method == 'POST':
            password = request.POST.get('password')
            if password == blog.password:
                return render(request, 'blog_details.html', {'blog': blog})
        return render(request, 'blog_password.html', {'blog_id': pk})
    return render(request, 'blog_details.html', {'blog': blog})

def blog_password(request):
    return render(request, 'blog_password.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

def add_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.blog = blog
            post.save()
            return redirect('blog_details', blog_id=blog_id)
    else:
        form = PostCreationForm()
    return render(request, 'add_post.html', {'form': form})

def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = post_id
            comment.save()
            return redirect('post_details', post_id=post_id)
    else:
        form = CommentCreationForm(initial={'author': request.user, 'post': post_id})
    return render(request, 'add_comment.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentCreationForm

def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_details', post_id=post_id)
    else:
        form = CommentCreationForm()
    return render(request, 'post_details.html', {'post': post, 'comments': comments, 'form': form})
