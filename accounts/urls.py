from django.urls import path
from . import views

urlpatterns = [
    path('profile/<slug:profile_slug>/',  views.ProfileView.as_view(),  name="profile"),
    path('profile/edit/<slug:profile_slug>/',  views.EditProfileView.as_view(),  name="edit-profile"),
    path("profile/<slug:profile_slug>/followers/add", views.AddFollowerView.as_view(), name="add-follower"),
    path("profile/<slug:profile_slug>/followers/remove", views.RemoveFollowerView.as_view(), name="remove-follower"),
    path("profile/<slug:profile_slug>/followers", views.ListFollowersView.as_view(),  name="followers")
]