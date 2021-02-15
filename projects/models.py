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
from django.db.models.signals import pre_save,post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    print(instance)
    new_filename = random.randint(1,3910209312)
    print(new_filename)
    name, ext = get_filename_ext(filename)
 
    print(name,ext)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    print(final_filename)
    return "project_pics/{user_name}/{file_name}_{final_filename}".format(
                final_filename=final_filename,
                user_name = instance.user,
                file_name = name
     )
# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug =models.SlugField(max_length=2000,null=True,blank=True)
    project_image = models.ImageField(upload_to=upload_image_path,blank=True,null=True)
    project_link = models.CharField(max_length=200,blank=True,null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('projects:project-detail', kwargs={"slug": self.slug})

@receiver(post_save, sender=Project)
def project_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        random_num = random.randint(1,3910209312)
        instance.slug   = slugify(instance.title)+'-'+str(random_num)
        instance.save()