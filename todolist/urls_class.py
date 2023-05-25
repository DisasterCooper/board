from django.urls import path

from . import views_class

#  /post/
urlpatterns = [

    # для view_class (Class Based View - CBV) вызвать '.as_view()'
    path('', views_class.PostsList.as_view(), name='home'),
    path('create/', views_class.CreatePost.as_view(), name='post_create'),
    # path('<int:post_id>/', views_class.show_post, name='post_show'),
    # path('<int:post_id>/edit/', views_class.edit_post, name='post_edit'),
    # path('<int:post_id>/delete/', views_class.delete_post, name='post_delete'),
]
