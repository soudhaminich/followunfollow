from django.contrib.sitemaps import Sitemap
from .models import Post
from django.shortcuts import reverse


class PostSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return Post.objects.filter(approved='Y')

    def lastmod(self, obj):
        return obj.date_posted


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['blog-about', 'policy', 'donate']

    def location(self, item):
        return reverse(item)
