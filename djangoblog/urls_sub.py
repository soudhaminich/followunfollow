from django.urls import path

from support import views as support_views

urlpatterns = [
    path('support/', support_views.SubDomainIndex.as_view(), name='index'),
]
