from django.urls import path
from . import views


urlpatterns = [
    path("",   views.LandingPage.as_view(),  name="landing"),
    path("home/",   views.HomeView.as_view(),  name="home"),
]
