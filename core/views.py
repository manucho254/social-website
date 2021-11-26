from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment
from django.contrib import messages
from .forms import CommentModelForm
from django.views import View


class LandingPage(View):
    def get(self, request,  *args,  **kwargs):
        return render(request,  "index.html",  {})

class HomeView(View):
    def get(self,  request,  *args,  **kwargs):
        posts = Post.objects.all()
        context = {
            "posts": posts,
        }
        return render(request,  "homepage.html",  context)
    