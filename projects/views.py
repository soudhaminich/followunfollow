from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import Project
from comments.forms import CommentForm
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from meta.views import Meta
# Create your views here.

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    queryset = Project.objects.filter(published=True)
