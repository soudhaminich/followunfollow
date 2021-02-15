from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
from blogs.models import Post
import os
import random
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from support.models import Question
from videos.models import Course


class Order(models.Model):
    course = models.ForeignKey(
        Course, null=True, blank=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(
        Question, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    payment = models.BooleanField(default=False)
    customer = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.customer.username) + ' ' + str(self.payment)
