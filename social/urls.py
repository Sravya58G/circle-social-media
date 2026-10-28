from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="form.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("post/", views.create_post, name="create_post"),
    path("like/<int:pk>/", views.like, name="like"),
    path("comment/<int:pk>/", views.comment, name="comment"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("bio/", views.bio, name="bio"),
    path("follow/<str:username>/", views.follow, name="follow"),
]
