from django.urls import path,re_path

from projects.views import (
                    ProjectListView
)

app_name = 'projects'
urlpatterns =[
    path('', ProjectListView.as_view(),name='project-list'),
    # path('<slug:slug>/', CourseDetailView.as_view(),name='course-detail'),
]