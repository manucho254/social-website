from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
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
        context = {
            "posts": posts,
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
    
    
class CreatePostView(View):
    def get(self,  request,  *args, **kwargs):
        form = PostModelForm()
        context = {
            "form": form
        }
        return render(request,  "post_create.html",  context)
    
    def post(self,  request,  *args,  **kwargs):
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("home")
            
        context = {
            "form": form
        }
        return render(request,  "post_create.html",  context)
    

class UpdatePostView(UpdateView):
    model = Post
    fields = ['caption','body', 'post_image', ]
    template_name = 'post_update.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail',  kwargs={'pk': pk})


class DeletePostView(DeleteView):
    pass

    