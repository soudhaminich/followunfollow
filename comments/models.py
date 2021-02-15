from django.db import models
from django.conf import settings
# from blogs.models import Post
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils.safestring import mark_safe
from markdown_deux import markdown
# Create your models here.
User = settings.AUTH_USER_MODEL


class CommentManager(models.Manager):

    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(
            content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):

    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    # comment = models.TextField(max_length=2000)
    comment = RichTextUploadingField(config_name='awesome_ckeditor')
    # post    = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    url = models.URLField(blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True,
                               on_delete=models.CASCADE, related_name='comment_parent')

    objects = CommentManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.user} commented {self.content_type} {self.comment} for {self.object_id}'

    def get_absolute_url(self):
        return reverse('comments:thread', kwargs={'id': self.id})

    @property
    def formatted_markdown(self):
        print(self.comment)
        return mark_safe(markdownify(self.comment))

    def get_markdown(self):
        content = self.comment
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def serialize(self):

        updated_time_format = self.timestamp
        updated_time_format = updated_time_format.strftime("%B %d %Y")
        return {
            "id": self.id,
            "comment": self.comment,
            "user": self.user.first_name,
            "image": self.user.profile.image.url,
            "updated_time": updated_time_format,
            "post_id": self.object_id
        }

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Reply(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(
        Comment, blank=True, null=True, on_delete=models.SET_NULL)
    replied = models.TextField(max_length=2000, blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} commented {self.comment.comment} '

    def serialize(self):

        updated_time_format = self.timestamp
        updated_time_format = updated_time_format.strftime("%B %d %Y")
        return {
            "id": self.comment.id,
            "comment": self.replied,
            "user": self.user.first_name,
            "image": self.user.profile.image.url,
            "updated_time": updated_time_format,
            "post_id": self.comment.object_id,
            "reply_id": self.id
        }
