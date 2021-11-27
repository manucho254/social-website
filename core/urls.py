from django.urls import path
from . import views


urlpatterns = [
    path("",   views.LandingPage.as_view(),  name="landing"),
    path("home/",   views.HomeView.as_view(),  name="home"),
    path("post/<int:pk>/",   views.PostDetailView.as_view(),  name="post-detail"),
    path("post/create/",  views.CreatePostView.as_view(), name="create-post"),
    path("post/update/<int:pk>/",  views.UpdatePostView.as_view(), name="update-post"),
]
