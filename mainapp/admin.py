from django.contrib import admin
from .models import Post,Comment,User,Tag,PostTag,Blog, SearchHistory

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(Blog)
admin.site.register(SearchHistory)

