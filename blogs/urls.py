from django.urls import path, re_path

from . import views
from blogs.views import (BlogView, AboutView, BlogDetailView,
                         CreatePostView, CreateCrudUser, BlogUpdate, UpdatePost,
                         PolicyView)
from django.contrib.auth.decorators import login_required


app_name = 'blogs'

urlpatterns = [

    path('', BlogView.as_view(), name='blog-home'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('tag/<slug:tag_slug>/', BlogView.as_view(), name='tag_by_category'),
    path('notification/', views.users_notification, name='send-notify'),
    path('post/create/', login_required(CreatePostView.as_view()), name='create'),
    path('post/<slug:slug>/edit/',
         login_required(UpdatePost.as_view()), name='edit'),
    path('post/delete/<slug:slug>/',
         views.delete_blog_post, name='post-delete'),
    path('about/', AboutView.as_view(), name='blog-about'),
    path('policy/', PolicyView.as_view(), name='policy'),
    path('delete/<post_id>/', views.blog_delete_post, name='delete'),
    path('donate/', views.donate, name='donate'),
    path('update/<slug:slug>/', BlogUpdate.as_view(), name='update'),

    path('test/', views.test, name='test'),
    path('favorite/<post_id>/<fav_id>/', views.favorite_like, name='favorite'),
    path('ajax/<post_id>/<fav_id>/', views.ajax_like, name='ajax-like'),
    path('ajax/crud/create/',  views.CreateCrudUser.as_view(),
         name='crud_ajax_create'),
    path('upload_test/', views.upload_test, name='upload_test'),
    path('create_post/', views.create_post, name='create_post'),
    path('create_story/', views.create_story, name='create_story'),
    #  re_path(r'^sign_s3/(?:file_name-(?P<file_name>\d+)/)?$', views.sign_s3,name='sign_s3'),
    #  path('sign_s3/<file_name>/<file_type>/', views.sign_s3,name='sign_s3'),
    #      path('generate_signed_url/', GetS3SignedUrl.as_view(), name='generate_signed_url'),
    # path('make_video_public/', Makes3VideoPublic.as_view(), name='make_video_public'),


    # path('email/',views.email, name='email'),
]
