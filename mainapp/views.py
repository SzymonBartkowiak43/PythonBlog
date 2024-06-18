from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Post, Comment, Tag, PostTag
from .forms import CustomUserCreationForm, BlogCreationForm, CaptchaTestForm, BlogEditForm, UserEditForm, CustomPasswordChangeForm, PostCreationForm, PostEditForm, CommentCreationForm, CommentEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import logging
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import logging
import os

logger = logging.getLogger('myapp')


def generate_pdf(request):
    buffer = io.BytesIO()  # Tworzymy bufor do przechowywania danych PDF-a

    # Tworzymy nowy dokument PDF w buforze
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Logi z aplikacji")  # Dodajemy tytuł dokumentu

    # Otwieramy plik z logami
    log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'debug.log'))
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            y = 700  # Początkowa pozycja Y dla tekstu

            for log in logs:
                if y < 50:  # Jeżeli dotrzemy do końca strony, dodajemy nową stronę
                    p.showPage()
                    y = 750  # Reset pozycji Y dla nowej strony
                    p.drawString(100, 750, "")  # Tytuł na nowej stronie

                p.drawString(100, y, log.strip())
                y -= 20  # Przesunięcie pozycji Y dla kolejnego wiersza tekstu
    except FileNotFoundError:
        logger.error(f"File not found: {log_file_path}")
        p.drawString(100, 700, "Log file not found.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='application/pdf')
def homepage(request):
    logger.info("Homepage view was called")
    return render(request, "home.html")


def register(request):
    logger.info("Register view was called")
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        captcha_form = CaptchaTestForm(request.POST)

        if user_form.is_valid() and captcha_form.is_valid():
            user = user_form.save()
            logger.info("New user registered")

            # Wyślij e-mail powitalny
            subject = 'Welcome to Our Site'
            message = f'Hi {user.first_name}, thank you for registering at our site.'
            recipient_list = [user.email]

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
                logger.info(f"Welcome email sent to {user.email}")
            except Exception as e:
                logger.error(f"Failed to send welcome email to {user.email}: {e}")

            return redirect('login')
        else:
            logger.warning("User registration failed: form invalid")
    else:
        user_form = CustomUserCreationForm()
        captcha_form = CaptchaTestForm()

    return render(request, "register.html", {"form": user_form, "captcha_form": captcha_form})




def blogs(request):
    logger.info("Blogs view was called")
    blogs = Blog.objects.all()
    return render(request, 'blogi.html', {'blogs': blogs})


def login_view(request):
    logger.info("Login view was called")
    if request.method == 'POST':
        captcha_form = CaptchaTestForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]

        if captcha_form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully")
                return redirect('homepage')
            else:
                logger.warning(f"Failed login attempt for user {username}")
                messages.error(request, "Invalid username or password.")
        else:
            logger.warning("Captcha validation failed")

    else:
        captcha_form = CaptchaTestForm()

    return render(request, "login.html", {"captcha_form": captcha_form})


@login_required
def BlogCreationView(request):
    logger.info("BlogCreationView was called")
    if request.method == "POST":
        form = BlogCreationForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user
            blog.save()
            logger.info(f"Blog created by user {request.user.username}")
            return redirect('homepage')
        else:
            logger.warning("Blog creation failed: form invalid")
    else:
        form = BlogCreationForm()
    return render(request, "utworz_blog.html", {"form": form})


@login_required
def BlogEditView(request, blog_id):
    logger.info(f"BlogEditView was called for blog_id {blog_id}")
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user != blog.owner:
        logger.warning(f"Unauthorized blog edit attempt by user {request.user.username}")
        return redirect('homepage')

    if request.method == 'POST':
        form = BlogEditForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            logger.info(f"Blog {blog_id} edited by user {request.user.username}")
            return redirect('blog_details', blog_id=blog_id)
        else:
            logger.warning(f"Blog edit failed for blog_id {blog_id}: form invalid")
    else:
        form = BlogEditForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})


@login_required
def BlogDeleteView(request, blog_id):
    logger.info(f"BlogDeleteView was called for blog_id {blog_id}")
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user == blog.owner:
        blog.delete()
        logger.info(f"Blog {blog_id} deleted by user {request.user.username}")
    else:
        logger.warning(f"Unauthorized blog delete attempt by user {request.user.username}")
    return redirect('blogs')


@login_required
def blog_details(request, blog_id):
    logger.info(f"Blog details view was called for blog_id {blog_id}")
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
    logger.info("Logout view was called")
    logout(request)
    logger.info(f"User {request.user.username} logged out")
    return redirect('homepage')


@login_required
def add_post(request, blog_id):
    logger.info(f"Add post view was called for blog_id {blog_id}")
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user != blog.owner:
        logger.warning(f"Unauthorized add post attempt by user {request.user.username}")
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
            logger.info(f"Post created by user {request.user.username} in blog {blog_id}")
            return redirect('blog_details', blog_id=blog_id)
        else:
            logger.warning(f"Post creation failed for blog_id {blog_id}: form invalid")
    else:
        form = PostCreationForm()
    return render(request, 'add_post.html', {'form': form, 'blog': blog})


@login_required
def PostEditView(request, post_id):
    logger.info(f"PostEditView was called for post_id {post_id}")
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        logger.warning(f"Unauthorized post edit attempt by user {request.user.username}")
        return redirect('homepage')

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            logger.info(f"Post {post_id} edited by user {request.user.username}")
            return redirect('post_details', post_id=post_id)
        else:
            logger.warning(f"Post edit failed for post_id {post_id}: form invalid")
    else:
        form = PostEditForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def PostDeleteView(request, post_id):
    logger.info(f"PostDeleteView was called for post_id {post_id}")
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        post.delete()
        logger.info(f"Post {post_id} deleted by user {request.user.username}")
        return redirect('blog_details', blog_id=post.blog.id)
    else:
        logger.warning(f"Unauthorized post delete attempt by user {request.user.username}")
    return redirect('homepage')


def post_details(request, post_id):
    logger.info(f"Post details view was called for post_id {post_id}")
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
                    logger.info(f"Password verified for private post {post_id} by user {request.user.username}")
                    return redirect('post_details', post_id=post_id)
                else:
                    logger.warning(
                        f"Incorrect password attempt for private post {post_id} by user {request.user.username}")
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
            logger.info(f"Comment added to post {post_id} by user {request.user.username}")
            return redirect('post_details', post_id=post_id)
        else:
            logger.warning(f"Comment creation failed for post {post_id}: form invalid")

    return render(request, 'post_details.html', {
        'post': post, 'comments': comments, 'form': form
    })




@login_required
def CommentEditView(request, comment_id):
    logger.info(f"CommentEditView was called for comment_id {comment_id}")
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        logger.warning(f"Unauthorized comment edit attempt by user {request.user.username}")
        return redirect('homepage')

    if request.method == 'POST':
        form = CommentEditForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            logger.info(f"Comment {comment_id} edited by user {request.user.username}")
            return redirect('post_details', post_id=comment.post.id)
        else:
            logger.warning(f"Comment edit failed for comment_id {comment_id}: form invalid")
    else:
        form = CommentEditForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})


@login_required
def CommentDeleteView(request, comment_id):
    logger.info(f"CommentDeleteView was called for comment_id {comment_id}")
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        post_id = comment.post.id
        comment.delete()
        logger.info(f"Comment {comment_id} deleted by user {request.user.username}")
        return redirect('post_details', post_id=post_id)
    return redirect('homepage')


def post_password(request, post_id):
    logger.info(f"Post password view was called for post_id {post_id}")
    return render(request, 'post_password.html', {'post_id': post_id})


@login_required
def edit_profile(request):
    logger.info(f"Edit profile view was called by user {request.user.username}")
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if user_form.is_valid():
            user_form.save()
            logger.info(f"User {request.user.username} updated their profile")
            messages.success(request, 'Twój profil został zaktualizowany pomyślnie')
            return redirect('edit_profile')
        else:
            logger.warning(f"Profile update failed for user {request.user.username}: form invalid")

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