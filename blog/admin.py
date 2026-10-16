from django.contrib import admin
from blog.models import Author, Profile, Category, Tag, Post, Comment

admin.site.register(Author)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
