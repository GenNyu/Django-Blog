from django.urls import path
from .views import home, create_post, post_detail, edit_post, my_posts, delete_post

urlpatterns = [
    path('', home, name = 'home'),
    path('create/', create_post, name = 'create_post'),
    path('my-posts/', my_posts, name='my_posts'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
]
