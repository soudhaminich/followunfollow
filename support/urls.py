from django.urls import path, re_path
from . import views
from support.views import (
    QuestionDetailView,
    CreateQuestion,
    UpdateQuestion,
    QuestionListView,
    PayTicket,
    QuestionListAllView
    #     QuestionListFilterView
)

app_name = 'support'

urlpatterns = [


    path('', QuestionListView.as_view(), name='question'),
    path('questions/', QuestionListAllView.as_view(), name='all-question'),
    path('notification/', views.notification, name='notification'),
    path('notidel/', views.notification_delete, name='notification_delete'),
    path('support/', views.question, name='question'),
    path('log_questions/', views.sub_question, name='sub_question'),
    path('questions/<slug:slug>/', QuestionDetailView.as_view(), name='detail'),
    path('question_update/<slug:slug>/', views.question_update, name='update'),
    path('ask/', CreateQuestion.as_view(), name='create'),
    path('create/', CreateQuestion.as_view(), name='create'),
    path('edit/<slug:slug>/', UpdateQuestion.as_view(), name='edit'),
    path('support/create/', CreateQuestion.as_view(), name='create'),
    path('support/questions/<slug:slug>/',
         QuestionDetailView.as_view(), name='detail'),
    path('suport/question/<object_id>/', views.question_comment,
         name='ques_comm'),
    path('question/answer/<object_id>/edit/<question_id>/', views.comment_edit,
         name='ques_answ_edit'),
    #     path('question/<category>/',
    #          QuestionListFilterView.as_view(), name='category_filter'),

    path('suport/question/<ques_comm_id>/delete/', views.question_comment_delete,
         name='question_comment_delete'),

    path('suport/question/<ques_comm_id>/edit/', views.question_comment_edit,
         name='question_comment_edit'),

    path('suport/answer/<comment_id>/<question_id>/', views.answer_verified,
         name='verified_answer'),
    path('question/vote/<comment_id>/<str:vote_type>/', views.vote_comment,
         name='vote_comment'),
    re_path(r'^tickets/(?P<slug>[0-9A-Za-z_\-]+)/pay/$',
            PayTicket.as_view(), name='ticket_pay'),

     path('support/multianswer/<comment_id>/<question_id>/', views.answer_verified,
         name='verified_answer'),
]
