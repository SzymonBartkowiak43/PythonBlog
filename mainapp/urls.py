from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('crtblog/', views.BlogCreationView, name='utworz_blog'),
    path('addpost/<int:blog_id>/', views.add_post, name='add_post'),  # Zaktualizowana ścieżka
    path('addcomment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/', views.post_details, name='post_details'),
    path('blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('blogpassword/', views.blog_password, name='blog_password'),
    path('blogs/', views.blogs, name='blogs'),
    path('logout/', views.logout_view, name='logout'),
]
