from django.urls import path
from . import views
urlpatterns = [
    path("", views.static_route, name="static_route"),

]
