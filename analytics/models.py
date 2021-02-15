from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .signals import object_viewed_signal
# from .utils import get_client_ip, get_client_location, get_client_city, get_client_flag, get_client_region
from support.models import Question
from blogs.models import Post
from tecsee.models import TecseeVideo

User = settings.AUTH_USER_MODEL
# Create your models here.


class ObjectViewed(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    ip_location = models.CharField(max_length=220, blank=True, null=True)
    ip_region = models.CharField(max_length=220, blank=True, null=True)
    ip_city = models.CharField(max_length=220, blank=True, null=True)
    ip_flag = models.CharField(max_length=2000, blank=True, null=True)
    # content_type = models.ForeignKey(
    #     ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE,  null=True)
    blog = models.ForeignKey(
        Post, on_delete=models.CASCADE,  null=True)
    video = models.ForeignKey(
        TecseeVideo, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return f'{self.question} viewed on {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']


class SuggestionFeedback(models.Model):
    content = models.TextField()
    email_id = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

def get_client_ip(request):
    x_forwarded_for  = request.META.get('HTTP_X_FORWARDED_FOR')
    # print(x_forwarded_for)
    # print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    
    return ip

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    # c_type = ContentType.objects.get_for_model(sender)  # instance.__class__
    # print(instance.__class__)
    # print(isinstance(instance, Post))
    print(instance)
    if isinstance(instance, Post):
        check_ip_exist = get_client_ip(request)
        check_ip_exist = ObjectViewed.objects.filter(ip_address=check_ip_exist,blog=instance)
        
        if check_ip_exist.count() == 0:
            if isinstance(instance, Post):
                user = None
                if request.user.is_authenticated:
                    user = request.user

                new_view_obj = ObjectViewed.objects.create(
                    user=user,
                    # content_type=c_type,
                    # object_id=instance.id,
                    ip_address=get_client_ip(request),
                    # ip_location=get_client_location(request),
                    # ip_region=get_client_region(request),
                    # ip_city=get_client_city(request),
                    # ip_flag=get_client_flag(request),
                    # question=instance,
                    blog=instance
                )
    if isinstance(instance, Question):
        check_ip_exist = get_client_ip(request)
        check_ip_exist = ObjectViewed.objects.filter(ip_address=check_ip_exist,question=instance)
        # print(check_ip_exist)
        if check_ip_exist.count() == 0:
            if isinstance(instance, Question):
                # print(instance)
                user = None
                if request.user.is_authenticated:
                    user = request.user

                new_view_obj = ObjectViewed.objects.create(
                    user=user,
                    # content_type=c_type,
                    # object_id=instance.id,
                    ip_address=get_client_ip(request),
                    # ip_location=get_client_location(request),
                    # ip_region=get_client_region(request),
                    # ip_city=get_client_city(request),
                    # ip_flag=get_client_flag(request),
                    question=instance,
                    # blog=instance
                )
    if isinstance(instance, TecseeVideo):
        check_ip_exist = get_client_ip(request)
        check_ip_exist = ObjectViewed.objects.filter(ip_address=check_ip_exist,video=instance)
        if check_ip_exist.count() == 0:
            if isinstance(instance, TecseeVideo):
                # print(instance)
                user = None
                if request.user.is_authenticated:
                    user = request.user

                new_view_obj = ObjectViewed.objects.create(
                    user=user,
                    # content_type=c_type,
                    # object_id=instance.id,
                    ip_address=get_client_ip(request),
                    # ip_location=get_client_location(request),
                    # ip_region=get_client_region(request),
                    # ip_city=get_client_city(request),
                    # ip_flag=get_client_flag(request),
                    video=instance,
                    # blog=instance
                )
                


object_viewed_signal.connect(object_viewed_receiver)


class PageViewed(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.url} viewed on {self.timestamp} by {self.user} using {self.ip_address}'


class Contact(models.Model):
    REASON_CHOICE = [('A', 'Ads'), ('T', 'Techion'),
                     ('T', 'Personal Training'), ('P', 'Project'), ('O', 'Other')]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    purpose = models.CharField(
        max_length=200, choices=REASON_CHOICE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
