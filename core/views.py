from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile
from django.http import HttpResponseRedirect
from django.db.models import Q
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
        logged_in_user = request.user
        posts = Post.objects.filter(author__profile__followers__in=[logged_in_user.id])
        paginator = Paginator(posts, 5) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = CommentModelForm()
        
        context = {
            "posts": posts,
            "page_obj": page_obj,
            "form": form
        }
        return render(request,  "homepage.html",  context)
    
    def post(self,  request, post_slug,  *args,  **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
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
        return render(request,  "partials/comment_form.html",  context)
    
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, post_slug,  *args,  **kwargs):
        post =  get_object_or_404(Post, post_slug=post_slug)
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
     
    def post(self,  request, post_slug,  *args,  **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
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
        return render(request,  "partials/comment_form.html",  context)
    
    
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
        slug = self.kwargs['post_slug']
        return reverse_lazy('post-detail',  kwargs={'post_slug': slug})
    
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
    
class CommentView(LoginRequiredMixin, View):
    def get(self,  request,  post_slug ,  *args, **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
        comments = Comment.objects.filter(post=post)
        template_name = "partials/comment_data.html"
        
        context = {
            "comments": comments,
            "post": post
        }
        
        return render(request,  template_name,  context)
    
class CommentCountView(LoginRequiredMixin, View):
    def get(self,  request,  post_slug ,  *args, **kwargs):
        post = get_object_or_404(Post, post_slug=post_slug)
        comments = Comment.objects.filter(post=post)
        template_name = "partials/comment_count.html"
        
        num_of_comments = len(comments)
        
        context = {
            "comments": comments,
            "post": post,
            "num_of_comments": num_of_comments
        }
        
        return render(request,  template_name,  context)
    
    
class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['message']
    template_name = 'comment_edit.html'
    
    def get_success_url(self):
        slug = self.kwargs['post_slug']
        return reverse_lazy('post-detail',  kwargs={'post_slug': slug})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    
    def get_success_url(self):
        slug = self.kwargs['post_slug']
        return reverse_lazy('post-detail',  kwargs={'post_slug': slug})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
class CommentLikeView(LoginRequiredMixin, View):
    def get(self,  request,  pk,  *args,  **kwargs):
        pass
    def post(self,  request,  pk,  *args,  **kwargs):
        pass
    
class CommentReplyView(LoginRequiredMixin, View):
    def get(self,  request,  pk,  *args,  **kwargs):
        pass
    def post(self,  request,  pk,  *args,  **kwargs):
        pass
        
#follow and unfollow views

class LikePostView(LoginRequiredMixin,  View):
    def get(self,  request, post_slug , *args, **kwargs):
        template_name = "partials/like_form.html"
        post = Post.objects.get(post_slug=post_slug)
        context = {
            "post": post
        }
        return render(request, template_name, context)
    
    def post(self, request, post_slug,  *args, **kwargs):
        post = Post.objects.get(post_slug=post_slug)
        
        is_like = False
        
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
            
        if is_like:
            post.likes.remove(request.user)
        
        return redirect("like-post",  post_slug=post_slug)
    
#search view   
class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        
        post_list = Post.objects.filter(Q(caption__icontains=query) | Q(author__username__icontains=query))
        profiles = Profile.objects.filter(Q(user__username__icontains=query))
        
        context = {
           "search_results": post_list,
           "profiles": profiles
        }
        
        return render(request, "search.html",  context)
    
    