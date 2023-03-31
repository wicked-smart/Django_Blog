from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("post/", views.post_blog, name="post_blog"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("drafts/", views.drafts, name="draft"),
    path("blog_detail/<int:blog_id>", views.blog_detail, name="detail"),
    path("<int:blog_id>/comments", views.post_comments, name="comments"),
    path("<int:blog_id>/reply", views.post_reply, name="replies"),
    path("<int:blog_id>/edit", views.edit_blog, name="edit"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout")
    
]