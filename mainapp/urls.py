from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('crtblog/', views.BlogCreationView, name='utworz_blog'),
    path('addpost/', views.add_post, name='dodaj_post'),
    path('addcomment/', views.add_comment, name='dodaj_comment'),
    path('post/<int:post_id>/', views.post_details, name='post_details'),
    path('blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('blogpassword/', views.blog_password, name='blogs'),
    path('blogs/', views.blogs, name='blogs'),
    path('logout/', views.logout_view, name='logout'),
]
