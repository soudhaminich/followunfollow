from django.urls import path

from . import views
from analytics.views import SuggestionCreateView

app_name = 'analytics'

urlpatterns =[

        path('',SuggestionCreateView.as_view(),name='suggestion'),
     
        ]
