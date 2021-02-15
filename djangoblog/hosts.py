from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns('',
                         host(r'www', settings.ROOT_URLCONF, name='www'),
                         host(r'support', 'support.staticurl',name="static_support"),
                         host(r'(?P<cat>\w+).*',
                              'support.categoryurl', name='category'),
                         )
