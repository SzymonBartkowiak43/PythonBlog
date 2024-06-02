from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('crtblog/', views.BlogCreationView, name='utworz_blog'),
    path('addpost/<int:blog_id>/', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.post_details, name='post_details'),
    path('post_password/<int:post_id>/', views.post_password, name='post_password'),
    path('blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('blogs/', views.blogs, name='blogs'),
    path('logout/', views.logout_view, name='logout'),
    path('blogs/<int:blog_id>/edit/', views.BlogEditView, name='edit_blog'),
    path('blogs/<int:blog_id>/delete/', views.BlogDeleteView, name='delete_blog'),
    path('post/<int:post_id>/edit/', views.PostEditView, name='edit_post'),
    path('post/<int:post_id>/delete/', views.PostDeleteView, name='delete_post'),
    path('comment/<int:comment_id>/edit/', views.CommentEditView, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.CommentDeleteView, name='delete_comment'),
]
