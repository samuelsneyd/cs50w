from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="post"),
    path("edit-post/<int:post_id>", views.edit_post, name='edit_post'),
    path("following", views.following_view, name="following"),
    path("u/<str:username>", views.user_profile_view, name="user_profile"),
    path("like/<int:post_id>", views.like_view, name="like"),
    path("follow/<int:user_id>", views.follow_view, name="follow")
]
