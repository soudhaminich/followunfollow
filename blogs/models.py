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
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from django.urls import reverse
from meta.models import ModelMeta
from taggit.managers import TaggableManager


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
    return "blog_pics/{author_name}/{file_name}_{final_filename}".format(
        final_filename=final_filename,
        author_name=instance.author,
        file_name=name
    )


def upload_video_poster(instance, filename):
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
    return "video_poster/{author_name}/{file_name}_{final_filename}".format(
        final_filename=final_filename,
        author_name=instance.author,
        file_name=name
    )


def upload_video(instance, filename):
    # print(instance)
    # print(filename)
    print(instance)
    print(instance.author)
    new_filename = random.randint(1, 100)
    print(new_filename)
    name, ext = get_filename_ext(filename)
    if ext == '.mp4':
        print(name, ext)
        final_filename = '{new_filename}{ext}'.format(
            new_filename=new_filename, ext=ext)
        print(final_filename)
        return "video/{author_name}/{file_name}_{final_filename}".format(
            final_filename=final_filename,
            author_name=instance.author,
            file_name=name
        )
        # return "video/instance.author/filename"


class PostQuerySet(models.QuerySet):
    def search(self, query):

        lookup = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(author__username__icontains=query)
        )

        return self.filter(lookup)


class PostManager(models.Manager):

    def get_queryset(self):

        return PostQuerySet(self.model, using=self._db)

    def get_by_post_id(self, slug):
        # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Post(ModelMeta, models.Model):
    APPROVED_CHOICE = [('Y', 'Approved'), ('N', 'Pending'), ]
    CATEGORY_CHOICE = [('P', 'Python'), ('D', 'Django'), ('S', 'SQL'),
                       ('Or', 'Oracle'), ('JS', 'Javascript'), ('O', 'Other')]
    title = models.CharField(max_length=2000)
    content = RichTextUploadingField()
    date_posted = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.CharField(
        max_length=1, choices=APPROVED_CHOICE, default='N')
    blog_image = models.ImageField(
        upload_to=upload_image_path, blank=True, null=True, default='default.jpg')
    slug = models.SlugField(max_length=2000, null=True, blank=True)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICE, default='P')
    video_upload = models.FileField(
        upload_to=upload_video, blank=True, null=True)
    video_poster = models.ImageField(
        upload_to=upload_video_poster, blank=True, null=True, default='default.jpg')
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    # timestamp                       = models.DateTimeField(auto_now_add=True)
    # updated                         = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    published_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    publish = models.BooleanField(default=False)
    path = models.TextField(blank=True, null=True)
    video_file_name = models.CharField(max_length=120, null=True, blank=True)
    tags = TaggableManager()
    # formatted_image = ImageSpecField(source='blog_image', format='JPEG',
    #         options={'quality': 90})

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_post_blog_image(self):
        instance = self
        qs = Post.objects.exclude(blog_image__isnull=True)
        return qs

    def get_absolute_url(self):
        return reverse("blogs:detail", kwargs={"slug": self.slug})

    _metadata = {
        'title': 'name',
        'content': 'abstract',
        'blog_image': 'get_meta_image',

    }

    def get_meta_image(self):
        if self.blog_image:
            return self.blog_image.url

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         random_num = random.randint(1,3910209312)
    #         self.slug = slugify(self.title)+'-'+str(random_num)
    #         super().save(self,*args, **kwargs)


@receiver(post_save, sender=Post)
def blog_post_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        random_num = random.randint(1, 3910209312)
        instance.slug = slugify(instance.title)+'-'+str(random_num)
        instance.save()
    # def get_absolute_url(self):
    #     return reverse('blogs:blog-home')


class TestUpload(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    video_upload = models.FileField(
        upload_to=upload_video, blank=True, null=True)

    def __str__(self):
        return self.author


class Favorite(models.Model):
    # COLOR_CHOICES = [
    #             ('R', 'red'),
    #             ('B', 'black')
    #             ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    add_favorite = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    # color_favorite  = models.CharField(
    #                     max_length=1,
    #                     choices=COLOR_CHOICES,
    #                     default='B',
    #                     )

    def __str__(self):
        return f'{self.id} {self.user} {self.post} {self.add_favorite}'


class FileItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=1)
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    @property
    def title(self):
        return str(self.name)


class FileTest(models.Model):
    file_test = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=1)

    def __str__(self):
        return self.file_test
