from django.urls import path

from blogs.views import BlogView, detail_blog, like_blog, analytics
app_name = 'blogs'

urlpatterns = [
    path('', BlogView.as_view(), name='list_blogs'),
    path('create/', BlogView.as_view(), name='create_blog'),
    path('<int:pk>/', BlogView.as_view(), name='update_delete_blog'),
    path('<int:pk>/detail/', detail_blog, name='detail_blog'),
    path('<int:pk>/like/', like_blog, name='like_blog'),
    path('analytics/', analytics, name='analytics'),
]