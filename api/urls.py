from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.new_post, name='post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('list/', views.post_list, name='list'),
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
]
