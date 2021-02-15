from django.contrib import admin

# Register your models here.
from .models import ObjectViewed, SuggestionFeedback, Contact


class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = [
        'question',
        'blog',
        'timestamp',
        'user',
        'ip_address',
        'ip_location',
        'ip_region',
        'ip_city',
        'ip_flag'
    ]
    search_fields = ['ip_address']
    list_filter = ['ip_location']


admin.site.register(ObjectViewed, ObjectViewedAdmin)
admin.site.register(SuggestionFeedback)
admin.site.register(Contact)
