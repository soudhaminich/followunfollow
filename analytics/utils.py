# from django.contrib.gis.geoip2 import GeoIP2

# g = GeoIP2()
from django.conf import settings
import requests
import json

IPSLACK_KEY = settings.IPSLACK_KEY




def get_client_ip(request):
    x_forwarded_for  = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    # print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip

def get_client_location(request):
    x_forwarded_for  = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    # print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    ip_address = ip
    URL = 'http://api.ipstack.com/'
    end_point = 'http://api.ipstack.com/'+str(ip_address)+'?access_key='+str(IPSLACK_KEY)
    response = requests.get(end_point)
    output = json.loads(response.text)
    if output:
        return output['country_name']

def get_client_region(request):
    x_forwarded_for  = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    # print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    ip_address = ip
    URL = 'http://api.ipstack.com/'
    end_point = 'http://api.ipstack.com/'+str(ip_address)+'?access_key='+str(IPSLACK_KEY)
    response = requests.get(end_point)
    output = json.loads(response.text)
    if output:
        return output['region_name']

def get_client_city(request):
    x_forwarded_for  = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    # print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    ip_address = ip
    URL = 'http://api.ipstack.com/'
    end_point = 'http://api.ipstack.com/'+str(ip_address)+'?access_key='+str(IPSLACK_KEY)
    response = requests.get(end_point)
    output = json.loads(response.text)
    if output:
        return output['city']

def get_client_flag(request):
    x_forwarded_for  = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    # print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    ip_address = ip
    URL = 'http://api.ipstack.com/'
    end_point = 'http://api.ipstack.com/'+str(ip_address)+'?access_key='+str(IPSLACK_KEY)
    response = requests.get(end_point)
    output = json.loads(response.text)
    if output:
        return output['location']['country_flag']