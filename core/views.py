from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import CommentModelForm,PostModelForm
from django.views import View
from django.views.generic import UpdateView,DeleteView


class LandingPage(View):
    def get(self, request,  *args,  **kwargs):
        return render(request,  "landing_page.html",  {})

class HomeView(LoginRequiredMixin ,View):
    def get(self,  request,  *args,  **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            "posts": posts,
            "page_obj": page_obj,
        }
        return render(request,  "homepage.html",  context)
    
class CommentView(LoginRequiredMixin,  View):
    def get(self,  request, pk , *args, **kwargs):
        template_name = "comment_form.html"
        post = Post.objects.get(pk=pk)
        form = CommentModelForm()
        
        context = {
            "post": post,
            "form": form
        }
        return render(request, template_name, context)
    
    def post(self, request, pk,  *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentModelForm(request.POST)
        comments = Comment.objects.filter(post=post)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }
        return render(request,  "homepage.html",  context)
    
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk,  *args,  **kwargs):
        post =  get_object_or_404(Post, pk=pk)
        form = CommentModelForm()
        comments = Comment.objects.filter(post=post)
        
        num_of_comments = len(comments)
        
        context = {
            "post": post,
            "form": form,
            "comments": comments,
             "num_of_comments": num_of_comments,
        }
        
        return render(request,  "post_detail.html",  context)
    
    def post(self,  request, pk,  *args,  **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = CommentModelForm(request.POST)
        comments = Comment.objects.filter(post=post)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            
        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }
        return render(request,  "comment_form.html",  context)
    
    
class CreatePostView(LoginRequiredMixin, View):
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
    

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['caption','body', 'post_image', ]
    template_name = 'post_update.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail',  kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    
class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['message']
    template_name = 'comment_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail',  kwargs={'pk': pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail',  kwargs={'pk': pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
#follow and unfollow views


class LikePostView(LoginRequiredMixin,  View):
    def get(self,  request, pk , *args, **kwargs):
        template_name = "like_form.html"
        post = Post.objects.get(pk=pk)
        context = {
            "post": post
        }
        return render(request, template_name, context)
    
    def post(self, request, pk,  *args, **kwargs):
        post = Post.objects.get(pk=pk)
        
        is_like = False
        
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
            
        if is_like:
            post.likes.remove(request.user)
        
        return redirect("like-post",  pk=pk)