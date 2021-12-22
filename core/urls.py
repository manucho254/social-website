from django.urls import path
from . import views

urlpatterns = [
    path("",   views.LandingPage.as_view(),  name="landing"),
    path("home/",   views.HomeView.as_view(),  name="home"),
    path("post/<int:pk>/",   views.PostDetailView.as_view(),  name="post-detail"),
    path("post/create/",  views.CreatePostView.as_view(), name="create-post"),
    path("post/update/<int:pk>/",  views.UpdatePostView.as_view(), name="update-post"),
    path("post/delete/<int:pk>/",  views.DeletePostView.as_view(),  name="delete-post"),
    path("post/<int:pk>/comment/",  views.CommentView.as_view(),  name="comments"),
    path("post/<int:pk>/comment/count",  views.CommentCountView.as_view(),  name="comment-count"),
    path("post/<int:post_pk>/comment/edit/<int:pk>/",   views.UpdateCommentView.as_view(), name="edit-comment"),
    path("post/<int:post_pk>/comment/delete/<int:pk>/", views.DeleteCommentView.as_view(), name="delete-comment"),
    path("post/<int:pk>/likes/add/", views.LikePostView.as_view(), name="like-post"),
]
