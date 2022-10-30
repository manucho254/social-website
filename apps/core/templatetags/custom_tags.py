from django import template
from django.shortcuts import render,redirect

from apps.core.forms import CommentModelForm
from apps.core.models import Notification, Post, Comment

register = template.Library()

@register.inclusion_tag('manuchosocial/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True)
    notification_data = {
        "notifications": notifications
    }

    return notification_data

# reply comment functionality 
@register.inclusion_tag('manuchosocial/comment_reply_form.html', takes_context=True)
def show_comment_reply_form(context, request, pk, post_slug):
        post = Post.objects.get(post_slug=post_slug)
        comment = Comment.objects.get(pk=pk)
        reply_form = CommentModelForm()
        
        context = {
            "reply_form": reply_form,
            "comment": comment,
            "post": post
        }
        return render(request,  "partials/comment_reply.html",  context)
        
def post(self,  request, post_slug, pk,  *args,  **kwargs):
    post = Post.objects.get(post_slug=post_slug)
    comment_parent = Comment.objects.get(pk=pk)
    form = CommentModelForm(request.POST)
    
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.parent = comment_parent
        new_comment.save()
    
    return redirect("post-detail",  post_slug=post_slug)