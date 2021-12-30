from django.contrib import admin
from .models import Comment, Post, Notification

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Notification)
