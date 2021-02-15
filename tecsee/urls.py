from django.urls import path, re_path
from django.conf.urls import url
from . import views
from tecsee.views import (
    TecseeListView,
    TecseeDetailView,
    MyView,
    Create
)
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import  storeUrl
app_name = 'tecsee'

urlpatterns = [

    path('create/', Create.as_view(), name='create'),
    #  path('<int:pk>/', views.detail, name='detail'),
    path('', TecseeListView.as_view(), name='all-videos'),
    # url(r'^create/$', login_required(MyView.as_view()), name='form'),
    #  re_path(r'^s3direct/', include('s3direct.urls')),
    #  path('store_url/',storeUrl,name="store_url"),
    path('<slug:slug>/', TecseeDetailView.as_view(), name='detail'),
    
    
]
