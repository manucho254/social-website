from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment
from django.contrib import messages
from .forms import CommentModelForm,PostModelForm
from django.views import View
from django.views.generic import CreateView,UpdateView,DeleteView


class LandingPage(View):
    def get(self, request,  *args,  **kwargs):
        return render(request,  "landing_page.html",  {})

class HomeView(View):
    def get(self,  request,  *args,  **kwargs):
        posts = Post.objects.all()
        form = PostModelForm()
        context = {
            "posts": posts,
            "form": form
        }
        return render(request,  "homepage.html",  context)
    
    def post(self,  request,  *args,  **kwargs):
        posts = Post.objects.all()
        form = PostModelForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
        context = {
            "posts": posts,
            "form":form
        }
        return render(request,  "homepage.html",  context)
    
    
class PostDetailView(View):
    def get(self, request, pk,  *args,  **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentModelForm()
        
        context = {
            "post": post,
            "form": form
        }
        
        return render(request,  "post_detail.html",  context)
    
    def post(self,  request, pk,  *args,  **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentModelForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
        context = {
            "posts": post,
            "form": form
        }
        return render(request,  "post_detail.html",  context)
    
class CreatePost(CreateView):
    pass

    