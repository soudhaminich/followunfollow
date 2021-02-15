from django.contrib import admin

# Register your models here.
from .models import (Profile,
                     UserFollower,
                     #  TechionProfile,
                     UserAction,
                     #  PointsLookup,
                     Techion)


class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'user',
    ]
    search_fields = ['user__username']


class TechionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserFollower)
# admin.site.register(TechionProfile)
admin.site.register(UserAction)
# admin.site.register(PointsLookup)
admin.site.register(Techion, TechionAdmin)
