from django.contrib import admin

# Register your models here.
from support.models import Question
from blogs.models import Post
from tecsee.models import TecseeVideo
from .models import Comment, Reply
from django.shortcuts import get_object_or_404


class CommentAdmin(admin.ModelAdmin):
    def question_title(self, obj):
        # print(type(obj.content_object))
        if isinstance(obj.content_object, Question):
            # print(obj.content_type)
            try:
                ques = Question.objects.get(id=obj.object_id)
                question = ques.title
               
            except:
                question = None
                
            return question
        elif isinstance(obj.content_object, Post):
            try:
                blog = Post.objects.get(id=obj.object_id)
                blog = blog.title
            except:
                blog =None
            return blog

        elif isinstance(obj.content_object, TecseeVideo):
            try:
                video = TecseeVideo.objects.get(id=obj.object_id)
                video = video.title
            except:
                video =None
            return video
    readonly_fields = ('created_date',)
    list_display = [
        'user',
        'comment',
        'object_id',
        'question_title'

    ]


admin.site.register(Comment, CommentAdmin)
# admin.site.register(Reply)
