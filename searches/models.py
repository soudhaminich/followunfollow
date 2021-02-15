from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class SearchQuery(models.Model):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} searched {self.query}'
