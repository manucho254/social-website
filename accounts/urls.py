from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/',  views.ProfileView.as_view(),  name="profile"),
    path('profile/edit/<int:pk>/',  views.EditProfileView.as_view(),  name="edit-profile"),
    path("profile/<int:pk>/followers/add", views.AddFollowerView.as_view(), name="add-follower"),
    path("profile/<int:pk>/followers/remove", views.RemoveFollowerView.as_view(), name="remove-follower"),
]