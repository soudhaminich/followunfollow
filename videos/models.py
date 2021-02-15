from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
import os
from PIL import Image
from imagekit.models import ImageSpecField
from django.db.models import Q
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    print(instance)
    new_filename = random.randint(1, 3910209312)
    print(new_filename)
    name, ext = get_filename_ext(filename)

    print(name, ext)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    print(final_filename)
    return "course_pics/{user_name}/{file_name}_{final_filename}".format(
        final_filename=final_filename,
        user_name=instance.user,
        file_name=name
    )


class VideoProject(models.Model):
    # APPROVED_CHOICE = [('Y','Approved'),('N','Pending'),]
    # CATEGORY_CHOICE = [('P','Python'),('D','Django'),('S','SQL'),('Or','Oracle'),('JS','Javascript'),('O','Other')]
    # title = models.CharField(max_length=2000)
    # content = RichTextUploadingField()
    # date_posted = models.DateTimeField(null=True,blank=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # approved = models.CharField(max_length=1, choices=APPROVED_CHOICE,default='N')
    # blog_image = models.ImageField(upload_to=upload_image_path,blank=True,null=True)
    # slug =models.SlugField(max_length=2000,null=True,blank=True)
    # category =models.CharField(max_length=100,choices=CATEGORY_CHOICE,default='P')
    # video_upload = models.FileField(upload_to=upload_video,blank=True,null=True)
    # video_poster= models.ImageField(upload_to=upload_video_poster,blank=True,null=True, default='default.jpg')
    # size                            = models.BigIntegerField(default=0)
    # file_type                       = models.CharField(max_length=120, null=True, blank=True)
    # # timestamp                       = models.DateTimeField(auto_now_add=True)
    # # updated                         = models.DateTimeField(auto_now=True)
    # uploaded                        = models.BooleanField(default=False)
    # active                          = models.BooleanField(default=True)
    # path  = models.TextField(blank=True, null=True)
    # video_file_name                            = models.CharField(max_length=120, null=True, blank=True)
    # # formatted_image = ImageSpecField(source='blog_image', format='JPEG',
    # #         options={'quality': 90})

    # objects = PostManager()

    # def __str__(self):
    #     return self.title
    project = models.CharField(max_length=2000)
    content = RichTextUploadingField()
    description = models.TextField(blank=True, null=True)
    uploaded = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class JustVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(VideoProject, on_delete=models.CASCADE)
    uploaded = models.BooleanField(default=False)
    video_file_name = models.CharField(max_length=120, null=True, blank=True)
    file_type = models.CharField(max_length=120, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=200)
    # description = models.TextField(max_length=2000, blank=True, null=True)
    description = RichTextUploadingField(
        blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=2000, null=True, blank=True)
    course_image = models.ImageField(
        upload_to=upload_image_path, blank=True, null=True)
    published = models.BooleanField(default=False)
    amount = models.FloatField(null=True, blank=True)
    paid_course = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('videos:course-detail', kwargs={"slug": self.slug})


class PartCourse(models.Model):
    part_name = models.CharField(max_length=2000)
    part_num = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    video_source = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.part_name

    def get_absolute_url(self):
        return reverse('videos:part-detail', kwargs={"slug": self.slug})


@receiver(post_save, sender=Course)
def video_course_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        random_num = random.randint(1, 3910209312)
        instance.slug = slugify(instance.name)+'-'+str(random_num)
        instance.save()


@receiver(post_save, sender=PartCourse)
def part_course_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        random_num = random.randint(1, 3910209312)
        instance.slug = slugify(instance.part_name)+'-'+str(random_num)
        instance.save()
