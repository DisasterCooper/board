from django.urls import path

from . import views_class

#  /posts/
urlpatterns = [

    # для view_class (Class Based View - CBV) вызвать '.as_view()'
    path('', views_class.PostsList.as_view(), name='home'),
    path('create/', views_class.CreatePost.as_view(), name='create'),
    path('users/', views_class.ProfileUsers.as_view(), name='users'),
    path('top-posts/', views_class.TopPosts.as_view(), name='top_posts'),
    path('<int:post_id>/', views_class.ShowPost.as_view(), name='show'),
    path('<int:post_id>/edit/', views_class.EditPost.as_view(), name='edit'),
    path('<int:post_id>/delete/', views_class.DeletePost.as_view(), name='delete'),
    path('<int:post_id>/comment/add/', views_class.CommentAdd.as_view(), name='comment_add'),
]
