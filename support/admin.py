from django.contrib import admin

# Register your models here.
from .models import (Question,
                     QuestionComment,
                     Answer,
                     BusinessType,
                     Order,
                     PointsLookup,
                     ReplyNotification)


class ReplyNotificationAdmin(admin.ModelAdmin):
    list_display = ('question', 'comment', 'user', 'author', 'replied_user')


class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'status',
        'priority',
        'approved'
    ]
    search_fields = ['status']
    list_filter = ['status', 'category']


admin.site.register(ReplyNotification, ReplyNotificationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionComment)
admin.site.register(Answer)
admin.site.register(BusinessType)
admin.site.register(Order)
admin.site.register(PointsLookup)
