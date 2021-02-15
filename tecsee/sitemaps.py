from django.contrib.sitemaps import Sitemap
from .models import TecseeVideo


class TecseeSitemap(Sitemap):
    changefreq = "always"
    priority = 0.9

    def items(self):
        return TecseeVideo.objects.filter(approved='Y')

    def lastmod(self, obj):
        return obj.created_date
