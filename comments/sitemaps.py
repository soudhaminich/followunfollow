from django.contrib.sitemaps import Sitemap
from .models import Comment

class CommentSitemap(Sitemap):
    def items(self):
        return Comment.objects.all()