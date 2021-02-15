from django.contrib.sitemaps import Sitemap
from .models import Question


class QuestionSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return Question.objects.filter(approved='Y')

    def lastmod(self, obj):
        return obj.date_posted
