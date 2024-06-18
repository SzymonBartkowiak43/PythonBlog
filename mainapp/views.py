from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog, Post, Comment, Tag, PostTag
from .forms import CustomUserCreationForm, BlogCreationForm, CaptchaTestForm, BlogEditForm, UserEditForm, CustomPasswordChangeForm, PostCreationForm, PostEditForm, CommentCreationForm, CommentEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def homepage(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        captcha_form = CaptchaTestForm(request.POST)
        user_form = CustomUserCreationForm(request.POST)

        if captcha_form.is_valid() and user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        captcha_form = CaptchaTestForm()
        user_form = CustomUserCreationForm()

    return render(request, "register.html", {"form": user_form, "captcha_form": captcha_form})




def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blogi.html', {'blogs': blogs})


def login_view(request):
    if request.method == 'POST':
        captcha_form = CaptchaTestForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]

        if captcha_form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return redirect('login')
    else:
        captcha_form = CaptchaTestForm()

    return render(request, "login.html", {"captcha_form": captcha_form})


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
    if request.user != blog.owner:
        return redirect('homepage')

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

    # Handle private post logic
    if post.is_private:
        if not request.user.is_authenticated:
            return redirect('login')

        password_verified = request.session.get(f'post_{post_id}_password_verified', False)

        if not password_verified:
            if request.method == 'POST' and 'password' in request.POST:
                password = request.POST.get('password')
                if password == post.password:
                    request.session[f'post_{post_id}_password_verified'] = True
                    return redirect('post_details', post_id=post_id)
                else:
                    return render(request, 'post_password.html', {'post_id': post_id, 'error': 'Incorrect password'})
            else:
                return render(request, 'post_password.html', {'post_id': post_id})

    # Handle comment form submission
    if request.method == 'POST' and not 'password' in request.POST:
        form = CommentCreationForm(request.POST, request.FILES)
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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Twój profil został zaktualizowany pomyślnie')
            return redirect('edit_profile')

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Update session to prevent logout
            messages.success(request, 'Twoje hasło zostało zmienione pomyślnie')
            return redirect('edit_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })