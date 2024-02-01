from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views

urlpatterns = [
    path('all_blogs/', views.get_all_blogs),
    path('blog_by_id/<int:blog_id>/', views.get_blog_by_id),
    path('update_blog/<int:blog_id>/', views.post_update_blog),
    path('add_blog/', views.post_add_blog),
    path('delete_blog/<int:blog_id>/', views.delete_blog_by_id),
]
