from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/',  views.ProfileView.as_view(),  name="profile"),
    path('profile/edit/<int:pk>/',  views.EditProfileView.as_view(),  name="edit-profile")
]