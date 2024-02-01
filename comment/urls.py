from django.urls import path
from . import views

urlpatterns = [
    path('all_comments/', views.get_all_comments),
    path('comment_by_id/<int:comment_id>', views.get_comment_by_id),
    path('add_comment/<int:blog_id>', views.post_add_comment),
    path('update_comment/<int:comment_id>/', views.post_update_comment),
    path('delete_comment/<int:comment_id>/', views.delete_comment_by_id),
    path('comment_by_blog_id/<int:blog_id>/', views.get_comments_by_blog_id),
]
