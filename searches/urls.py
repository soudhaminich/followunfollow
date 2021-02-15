from django.urls import path,re_path

from searches.views import SearchView


app_name = 'searches'

urlpatterns =[

        path('',SearchView.as_view(),name='search'),

        
    ]