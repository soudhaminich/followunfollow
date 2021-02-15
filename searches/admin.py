from django.contrib import admin

# Register your models here.
from .models import SearchQuery


class SearchQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

admin.site.register(SearchQuery, SearchQueryAdmin)


