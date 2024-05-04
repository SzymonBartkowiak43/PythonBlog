from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    date_of_registration = models.DateField()
    role = models.CharField(max_length=255)




class Blog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_creation = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_creation = models.DateField()
    visibility = models.CharField(max_length=20)
    password = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    date_of_creation = models.DateField()

class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, through='PostTag')

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)
    date_of_search = models.DateField()

