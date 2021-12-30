from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import Profile
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
        template_name = "manuchosocial/landing_page.html"
        return render(request, template_name,  {})

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
        return render(request,  "manuchosocial/homepage.html",  context)
    
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
        post =  Post.objects.get(post_slug=post_slug)
        form = CommentModelForm()
        comments = Comment.objects.filter(post=post)
        
        num_of_comments = len(comments)
        
        context = {
            "post": post,
            "form": form,
            "comments": comments,
             "num_of_comments": num_of_comments,
        }
        
        return render(request,  "manuchosocial/post_detail.html",  context)
     
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
    def get(self, request, *args , **kwargs):
        form = PostModelForm()
        context = {
            "form": form
        }
        return render(request,  "manuchosocial/post_create.html",  context)
    
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
        return render(request,  "manuchosocial/post_create.html",  context)
    

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['caption','body', 'post_image', ]
    template_name = 'manuchosocial/post_update.html'
    
    def get_success_url(self):
        slug = self.kwargs['post_slug']
        return reverse_lazy('post-detail',  kwargs={'post_slug': slug})
    
    # overiding the get_object() method to get the desired object from database
    def get_object(self, queryset=None):
        return Post.objects.get(post_slug=self.kwargs.get("post_slug"))
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "manuchosocial/post_delete.html"
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        return Post.objects.get(post_slug=self.kwargs.get("post_slug"))
    
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
        post = Post.objects.get(post_slug=post_slug)
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
    template_name = 'manuchosocial/comment_edit.html'
    
    def get_success_url(self):
        slug = self.kwargs['post_slug']
        return reverse_lazy('post-detail',  kwargs={'post_slug': slug})
      
    # overiding the get_object() method to get the desired object from database
    def get_object(self, queryset=None):
        return \
            Post.objects.get(post_slug=self.kwargs.get("post_slug")) \
            and  Comment.objects.get(pk=self.kwargs.get("pk"))
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "manuchosocial/comment_delete.html"
    
    def get_success_url(self):
        slug = self.kwargs['post_slug']
        return reverse_lazy('post-detail',  kwargs={'post_slug': slug})
    
    def get_object(self, queryset=None):
        return \
            Post.objects.get(post_slug=self.kwargs.get("post_slug")) \
            and  Comment.objects.get(pk=self.kwargs.get("pk"))

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
  
#like comment 
class CommentLikeView(LoginRequiredMixin, View):
    def get(self,  request, pk , *args, **kwargs):
        template_name = "partials/comment_like_form.html"
        comment = Comment.objects.get(pk=pk)
        context = {
            "comment": comment
        }
        return render(request, template_name, context)
    
    def post(self, request, pk,  *args, **kwargs):
        comment = Comment.objects.get(pk=pk)
        
        is_like = False
        
        for like in comment.liked.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            comment.liked.add(request.user)
            
        if is_like:
            comment.liked.remove(request.user)
        
        return redirect("like-comment",  pk=pk)
    
class CommentReplyView(LoginRequiredMixin, View):
    def get(self, request, post_slug , pk, *args,  **kwargs):
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

#follow and unfollow views

class LikePostView(LoginRequiredMixin,  View):
    def get(self,  request, post_slug , *args, **kwargs):
        template_name = "partials/post_like_form.html"
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
        template_name = "manuchosocial/search.html"
        
        context = {
           "search_results": post_list,
           "profiles": profiles
        }
        
        return render(request, template_name ,  context)
    
    