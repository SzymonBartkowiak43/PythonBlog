from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog, Post, Comment, Tag, PostTag
from .forms import CustomUserCreationForm, BlogCreationForm, BlogEditForm, PostCreationForm, PostEditForm, CommentCreationForm, CommentEditForm


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


@login_required
def BlogEditView(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user != blog.owner:
        return redirect('homepage')

    if request.method == 'POST':
        form = BlogEditForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_details', blog_id=blog_id)
    else:
        form = BlogEditForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})


@login_required
def BlogDeleteView(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user == blog.owner:
        blog.delete()
    return redirect('blogs')


@login_required
def blog_details(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    posts = Post.objects.filter(blog=blog)

    tag_id = request.GET.get('tag')
    if tag_id:
        posts = posts.filter(posttag__tag_id=tag_id)

    tags = Tag.objects.all()
    comment_form = CommentCreationForm()
    return render(request, 'blog_details.html',
                  {'blog': blog, 'posts': posts, 'comment_form': comment_form, 'tags': tags})


def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required
def add_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.blog = blog
            post.save()
            form.save_m2m()
            tags = form.cleaned_data['tags']
            new_tags = form.cleaned_data['new_tags']

            for tag in tags:
                PostTag.objects.create(post=post, tag=tag)

            if new_tags:
                new_tag_names = [tag.strip() for tag in new_tags.split(',')]
                for name in new_tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    PostTag.objects.create(post=post, tag=tag)

            return redirect('blog_details', blog_id=blog_id)
    else:
        form = PostCreationForm()
    return render(request, 'add_post.html', {'form': form, 'blog': blog})


@login_required
def PostEditView(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('homepage')

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', post_id=post_id)
    else:
        form = PostEditForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def PostDeleteView(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('blog_details', blog_id=post.blog.id)


def post_details(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.order_by('date_of_creation')
    form = CommentCreationForm()

    if post.is_private:
        if not request.user.is_authenticated:
            return redirect('blog_password')
        else:
            if post.author != request.user:
                return redirect('blog_password')

        password = request.POST.get('password')
        if password != post.password:
            return render(request, 'post_password.html', {'post_id': post_id})

    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_details', post_id=post_id)

    return render(request, 'post_details.html', {
        'post': post, 'comments': comments, 'form': form
    })


@login_required
def CommentEditView(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('homepage')

    if request.method == 'POST':
        form = CommentEditForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_details', post_id=comment.post.id)
    else:
        form = CommentEditForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})


@login_required
def CommentDeleteView(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        post_id = comment.post.id
        comment.delete()
        return redirect('post_details', post_id=post_id)
    return redirect('homepage')


def post_password(request, post_id):
    return render(request, 'post_password.html', {'post_id': post_id})
