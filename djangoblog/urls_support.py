from django.urls import path

from support import views as support_views

urlpatterns = [
    path('domain/', support_views.CustomIndex.as_view(), name='index'),
]
