from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .serializers import (
    PostDetailSerializer,
    )
from rest_framework.permissions import (
    IsAuthenticated
)
from blogs.models import Post


def postdetail(request):
    return render(request, 'blogs/blog_detail_api.html', {})



class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # permission_classes = [IsAuthenticated]
