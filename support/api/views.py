from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .serializers import (
    QuestionSerializer,
)
from rest_framework.permissions import (
    IsAuthenticated
)
from support.models import Question
from rest_framework import viewsets


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'slug'
