from django.urls import path
from . import views


urlpatterns = [
    path('view_all', views.index, name='index'),
    path('view_single/<int:post_id>', views.view_post, name='view_post'),
    path('create_post', views.create_post, name='c_post'),
    path('new_comment/<int:post_id>', views.new_comment, name='new_comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
]
