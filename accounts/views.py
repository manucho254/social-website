from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Profile
from core.models import  Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from django.views.generic import UpdateView,DeleteView

class ProfileView(LoginRequiredMixin, View):
    def get(self,  request, profile_slug,*args,  **kwargs):
        profile = Profile.objects.get(profile_slug=profile_slug)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        
        followers = profile.followers.all()
        following =  profile.following.all()
        
        if len( following ) == 0:
            followed = False
            
        for follower in following:
            if follower == profile.user:
                followed = True
                break
        else:
            followed = False
        
        if len(followers) == 0:
            is_following = False
        
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
                
        number_of_followers = len(followers)
        num_following = len(following)
        
        context = {
            'profile': profile,
            'user': user,
            'posts' : posts,
            'number_of_followers' :  number_of_followers,
            'is_following': is_following,
            "num_following" :  num_following,
            "followed":  followed
            
        }
        
        return render(request,  "profiles/profile.html",  context)
    
class EditProfileView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Profile
    fields = ["first_name","last_name","bio","birthday","location","gender","profile_image"]
    
    template_name = "profiles/profile_edit.html"
    
    def get_success_url(self):
        slug = self.kwargs["profile_slug"]
        return reverse_lazy('profile', kwargs={"profile_slug": slug})
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    
# adding a follower

class AddFollowerView(LoginRequiredMixin,  View):
    def get(self, request, profile_slug ,  *args,  **kwargs):
        
        profile = Profile.objects.get(profile_slug=profile_slug)
        
        template_name = "partials/follow_unfollow.html"
        
        context = {
           "profile": profile
        }

        return render(request, template_name,  context)
        
    def post(self, request, profile_slug,  *args, **kwargs):
        profile = Profile.objects.get(profile_slug=profile_slug)
        profile.followers.add(request.user)
        profile.following.add(profile.user)
        
        return redirect("profile",  profile_slug=profile_slug)
       
    
class RemoveFollowerView(LoginRequiredMixin,  View):
    def get(self, request, profile_slug ,  *args,  **kwargs):
        
        profile = Profile.objects.get(profile_slug=profile_slug)
        
        template_name = "partials/follow_unfollow.html"
        
        context = {
           "profile": profile
        }

        return render(request, template_name,  context)
        
    def post(self, request, profile_slug,  *args, **kwargs):
        profile = Profile.objects.get(profile_slug=profile_slug)
        profile.followers.remove(request.user)
        profile.following.remove(profile.user)
        
        return redirect("profile",  profile_slug=profile_slug)
    
class ListFollowersView(LoginRequiredMixin,  View):
    def get(self,  request, profile_slug , *args, **kwargs):
        profile = Profile.objects.get(profile_slug=profile_slug)
        followers = profile.followers.all()
        
        context = {
            "profile": profile,
            "followers": followers
        }
        
        return render(request,  "profiles/followers.html",  context)