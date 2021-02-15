from django.urls import path, re_path

from . import views

app_name = 'comments'

urlpatterns = [

    path('<post_id>/', views.comment_view, name='comment_view'),
    path('question/<object_id>/', views.comment_question_view,
         name='comment_question_view'),
    path('e/question/<int:object_id>/', views.reply_question_edit,
         name='reply_question_edit'),
    # re_path(r'^(?P<klass>\w+)/$', views.comment_view,name='comment_view'),
    path('testing/<post_id>', views.comment_test, name='comment_test'),
    path('reply/<post_id>', views.reply, name='reply'),
    path('reply_comment/<comment_id>/<post_id>',
         views.reply_comment, name='reply_comment'),
    path('comment_list/<content>/', views.comment_list, name='comment_list'),
    path('comment_delete/<comment_id>/<klass>',
         views.comment_delete, name='comment_delete'),
    path('reply_delete/<reply_id>/<klass>',
         views.reply_delete, name='reply_delete'),
     path('tecsee/<object_id>/', views.comment_tecsee_view, name='comment_tecsee_view'),
    # re_path(r'^comment_list/<comment_id>', views.comment_list,name='comment_list'),
]
