from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from taggit.managers import TaggableManager
from django.db.models.signals import pre_save, post_save, post_delete
import random
from django.utils.text import slugify
from django.db.models import Q
from comments.models import Comment
from ckeditor_uploader.fields import RichTextUploadingField
from s3direct.fields import S3DirectField
# Create your models here.


class TecseeQuerySet(models.QuerySet):
    def search(self, query):

        lookup = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) 
        )

        return self.filter(lookup).exclude(approved='N')


class TecseeManager(models.Manager):

    def get_queryset(self):

        return TecseeQuerySet(self.model, using=self._db)

    def get_by_tecsee_id(self, slug):
        # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class TecseeVideo(models.Model):
    APPROVED_CHOICE = [('Y', 'Approved'), ('N', 'Pending'), ]
    title = models.CharField(max_length=500)
    description = RichTextUploadingField(config_name='awesome_ckeditor')
    image = S3DirectField(dest='destination')
    video = S3DirectField(dest='destination')
    # image = models.CharField(max_length=200)
    # video = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=2000, null=True, blank=True)
    approved = models.CharField(
        max_length=1, choices=APPROVED_CHOICE, default='Y')
    duration = models.CharField(max_length=100,null=True, blank=True)
    tags = TaggableManager()

    objects = TecseeManager()

    def __str__(self):
        return str(self.title) + 'Test' 

    def get_absolute_url(self):
        return reverse("tecsee:detail", kwargs={"slug": self.slug})

    # def get_absolute_url(self):
    #     return reverse('tecsee:detail', kwargs={'pk': self.pk})

    @ property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs


@receiver(post_save, sender=TecseeVideo)
def tecsee_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        random_num = random.randint(1, 3910209312)
        instance.slug = slugify(instance.title)+'-'+str(random_num)
        instance.save()
