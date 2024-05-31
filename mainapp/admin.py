from django.contrib import admin
from .models import Post,Comment,Profile,Tag,PostTag,Blog, SearchHistory




class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'date_of_registration', 'role')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)
    fieldsets = (
        (None, {
            'fields': ('user', 'age', 'role')
        }),
        ('Dates', {
            'fields': ('date_of_registration',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_of_registration',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'date_of_creation')
    search_fields = ('title', 'owner__username')
    list_filter = ['date_of_creation']
    fieldsets = (
        (None, {
            'fields': ('owner', 'title', 'description')
        }),
    )
    readonly_fields = ('date_of_creation',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_of_creation', 'blog')
    search_fields = ('title', 'author__username', 'blog__title')
    list_filter = ('date_of_creation', 'blog')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'blog')
        }),
        ('Optional Fields', {
            'classes': ('collapse',),
            'fields': ('password', 'image')
        }),
    )
    readonly_fields = ('date_of_creation',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date_of_creation', 'content')
    search_fields = ('post__title', 'author__username', 'content')
    list_filter = ('date_of_creation',)
    readonly_fields = ('date_of_creation',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PostTagAdmin(admin.ModelAdmin):
    list_display = ('post', 'tag')
    search_fields = ('post__title', 'tag__name')

class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_query', 'date_of_search')
    search_fields = ('user__username', 'search_query')
    list_filter = ('date_of_search',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PostTag, PostTagAdmin)
admin.site.register(SearchHistory, SearchHistoryAdmin)