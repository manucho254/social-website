from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Profile
from core.models import  Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from django.views.generic import UpdateView,DeleteView

class ProfileView(LoginRequiredMixin, View):
    def get(self,  request, pk,*args,  **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        
        context = {
            'profile': profile,
            'user': user,
            'posts' : posts
        }
        
        return render(request,  "profile.html",  context)