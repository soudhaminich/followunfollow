from django.urls import path
from . import views
from .views import PostDetailAPIView

urlpatterns = [
    path('post/<pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('detail/', views.postdetail, name='post-detail-api'),
]
