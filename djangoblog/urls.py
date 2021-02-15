"""bikeysight URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from users import views as user_views
from users.forms import PasswordReset
from users.views import ViewUserProfile, ProfileView,follow_unfollow_profile
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from searches.views import search_query

from django.contrib.sitemaps.views import sitemap
# ..Adding for media directory
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views
from django.views.generic.base import TemplateView
from blogs.views import (FilePolicyAPI,
                         FileUploadCompleteHandler,
                         donate,
                         PolicyView,
                         AboutView,
                         handler500)
from comments.views import comment_test, ConfirmNotification
from blogs.sitemaps import PostSitemap, StaticViewSitemap
from comments.sitemaps import CommentSitemap
from support.sitemaps import QuestionSitemap
from analytics.views import ContactCreateView
from tecsee.sitemaps import TecseeSitemap
from .handlers import *

sitemaps = {
    'posts': PostSitemap,
    'questions': QuestionSitemap,
    'static': StaticViewSitemap,
    'videos': TecseeSitemap
}

urlpatterns = [
    path('donate/', donate, name='donate'),
     path('s3direct/', include('s3direct.urls')),
    path('error/500/', handler500),
    path('policy/', PolicyView.as_view(), name='policy'),
    path('about/', AboutView.as_view(), name='blog-about'),
    path('api/', include("blogs.api.urls")),
    path('api/question/', include("support.api.urls")),
    path('blog/', include('blogs.urls')),
    path('tecsee/', include('tecsee.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('accounts/', include('allauth.urls')),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('', include('support.urls')),
    path('suggestion/', include('analytics.urls')),
    path('inbox/notifications/', include('notifications.urls')),
    path('u/', include('users.urls')),
    path('markdownx/', include('markdownx.urls')),

    path('ckeditor/upload/', views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', views.browse, name='ckeditor_browse'),
    path('search/', include('searches.urls')),
    path('comment/', include('comments.urls')),
    path('videos/', include('videos.urls')),
    path('projects/', include('projects.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordReset, template_name='users/registration/password_reset_form.html',
                                                                 html_email_template_name='users/registration/password_reset_email.html'),

         name='password_reset'),


    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/registration/password_reset_done.html'), name='password_reset_done'),


    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),


    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    path('register/', user_views.register, name='register'),
    path('forgot-password/', user_views.forgot_password, name='forgot_password'),


    path('activate/<uidb64>/<token>/',
         user_views.activate, name='activate'
         ),



    path('view_user_profile/<int:pk>/',
         login_required(ViewUserProfile.as_view()), name='view-user-profile'),
    path('teckiyadmin/', admin.site.urls),

    path('upload/', TemplateView.as_view(template_name='blogs/upload.html'),
         name='upload-home'),
    path('api/files/policy/', FilePolicyAPI.as_view(), name='upload-policy'),
    path('api/files/complete/', FileUploadCompleteHandler.as_view(),
         name='upload-complete'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('ws/notifs/confirm/', ConfirmNotification.as_view(), name='confirm-notify'),
    path('switch_follow/', follow_unfollow_profile,
         name='follow-unfollow-view'),

]


# This is for media only for dev purpose
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
