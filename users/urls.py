from django.urls import path, re_path

from . import views
from users.views import ProfileView, ViewUserProfile, follow_unfollow_profile
from django.contrib.auth.decorators import login_required


app_name = 'users'

urlpatterns = [
    
#     path('<pk>/',ProfileDetailView.as_view(),name='profile-detail-view'),

    
    re_path('(?P<username>[-\w.]+)/summary/$',
            views.profilesummary, name='profilesummary'),
    re_path('(?P<username>[-\w.]+)/post/$',
            views.profilepost, name='profilepost'),
    re_path('(?P<username>[-\w.]+)/ticket/$',
            views.profileticket, name='profileticket'),
    re_path('(?P<username>[-\w.]+)/techion/$',
            views.profiletechion, name='profiletechion'),
    re_path('(?P<username>[-\w.]+)/video/$',
            views.profilevideos, name='profilevideo'),
    re_path('edit/(?P<username>[-\w.]+)/$',
            ProfileView.as_view(), name='edit'),
    re_path('(?P<username>[-\w.]+)/$',
            views.profilesummary, name='profile'),
    
]

# urlpatterns =[

#   path('view_profile/<int:pk>/', login_required(UserProfileView.as_view()),name='view-profile'),

#     ]