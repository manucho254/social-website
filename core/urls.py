from django.urls import path
from . import views

urlpatterns = [
    path("",   views.LandingPage.as_view(),  name="landing"),
    path("home/",   views.HomeView.as_view(),  name="home"),
    path("post/create-post/",  views.CreatePostView.as_view(), name="create-post"),
    path("post/<slug:post_slug>/",   views.PostDetailView.as_view(),  name="post-detail"),
    path("post/update/<slug:post_slug>/",  views.UpdatePostView.as_view(), name="update-post"),
    path("post/delete/<slug:post_slug>/",  views.DeletePostView.as_view(),  name="delete-post"),
    path("post/<slug:post_slug>/comment/",  views.CommentView.as_view(),  name="comments"),
    path("post/<slug:post_slug>/comment/count/",  views.CommentCountView.as_view(),  name="comment-count"),
    path("post/<slug:post_slug>/comment/edit/<int:pk>/",   views.UpdateCommentView.as_view(), name="edit-comment"),
    path("post/<slug:post_slug>/comment/delete/<int:pk>/", views.DeleteCommentView.as_view(), name="delete-comment"),
    path("post/<slug:post_slug>/comment/<int:pk>/reply", views.CommentReplyView.as_view(), name="comment-reply"),
    path("post/<int:pk>/comment/like/add/", views.CommentLikeView.as_view(), name="like-comment"),
    path("post/<slug:post_slug>/likes/add/", views.LikePostView.as_view(), name="like-post"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("notification/<int:notification_pk>/post/<slug:post_slug>/", views.PostNotificationView.as_view(),  name="post-notification"),
    path("notification/<int:notification_pk>/profile/<slug:profile_slug>/", views.FollowNotificationView.as_view(),  name="follow-notification"),
    path("notification/delete/<int:notification_pk>/", views.RemoveNotificationView.as_view(),  name="remove-notification"),
    path("inbox/",  views.ListThreadsView.as_view(),  name="inbox"),
    path("inbox/create-thread/",  views.CreateThreadView.as_view(),  name="create-thread"),
    path("inbox/<int:pk>/",  views.MessegeView.as_view(),  name="thread"),
]
