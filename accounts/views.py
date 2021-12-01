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
        
        return render(request,  "profiles/profile.html",  context)
    
class EditProfileView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Profile
    fields = "__all__"
    template_name = "profiles/profile_edit.html"
    
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy('profile', kwargs={"pk": pk})
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user