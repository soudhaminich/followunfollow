from django.urls import path, re_path

from videos.views import (
    CourseListView,
    CourseDetailView,
    PartDetailView
)
from . import views

app_name = 'videos'
urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('o/process_order/', views.process_order, name='checkout'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('checkout/<slug:slug>/', views.checkout, name='checkout'),

    # re_path('(?P<course>[\w-]+)/(?P<slug>[\w-]+)/$',
    #         views.partdetailview, name='part-detail'),

]
