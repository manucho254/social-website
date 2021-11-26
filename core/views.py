from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Comment
from django.contrib import messages
from .forms import CommentModelForm,PostModelForm
from django.views import View
from django.views.generic import CreateView,UpdateView,DeleteView


class LandingPage(View):
    def get(self, request,  *args,  **kwargs):
        return render(request,  "index.html",  {})

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
    
class CreatePost(CreateView):
    pass
    