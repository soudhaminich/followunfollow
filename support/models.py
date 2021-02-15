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


class QuestionQuerySet(models.QuerySet):
    def search(self, query):

        lookup = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(category__icontains=query)
        )

        return self.filter(lookup).exclude(approved='N')


class QuestionManager(models.Manager):

    def get_queryset(self):

        return QuestionQuerySet(self.model, using=self._db)

    def get_by_question_id(self, slug):
        # Product.objects == self.get_queryset()
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Question(ModelMeta, models.Model):
    APPROVED_CHOICE = [('Y', 'Approved'), ('N', 'Pending'), ]
    CATEGORY_CHOICE = [('python', 'Python'), ('django', 'Django'), ('sql', 'SQL'), ('postgresql', 'PostgreSQL'), ('oracle', 'Oracle'), ('mysql', 'MYSQL'),
                       ('javascript', 'Javascript'), ('java', 'Java'),  ('vuejs', 'VueJS'), ('html', 'HTML'), ('css', 'CSS'), ('unix', 'Unix'), ('shellscript', 'Shell Script'), ('other', 'Other')]
    STATUS_CHOICE = [('I', 'In-Progress'), ('O', 'Opened'),
                     ('C', 'Closed'), ('D', 'Duplicate'), ('N', 'Not Resolved')]
    SHOW_CHOICE = [('PR', 'Private'), ('PU', 'Public')]
    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'
    PRIORITY_HIGH_PENDING = 'HP'
    PRIORITY_URGENT = 'U'
    PRIORITY_URGENT_PENDING = 'UP'
    AVAILABLE_PRIORITY_CHOICES = [(PRIORITY_LOW, 'Low'), (PRIORITY_MEDIUM, 'Medium'),
                                  (PRIORITY_HIGH, 'High'), (PRIORITY_URGENT, 'Urgent')]
    PRIORITY_CHOICE = AVAILABLE_PRIORITY_CHOICES + [(PRIORITY_HIGH_PENDING, 'High (pending)'),
                                                    (PRIORITY_URGENT_PENDING, 'Urgent (pending)')]
    TYPE_CHOICE = [('Q', 'Question'), ('P', 'Problem'), ('T', 'Task')]
    title = models.CharField(max_length=2000)
    content = RichTextUploadingField(config_name='awesome_ckeditor')
    date_posted = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    approved = models.CharField(
        max_length=1, choices=APPROVED_CHOICE, default='Y')
    slug = models.SlugField(max_length=2000, null=True, blank=True)
    ticket_type = models.CharField(
        max_length=200, choices=TYPE_CHOICE, blank=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICE, default='P')
    video = models.CharField(max_length=2000, default='N')
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=200, choices=STATUS_CHOICE, default='O')
    show_ques = models.CharField(
        max_length=20, choices=SHOW_CHOICE, default='PU')
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICE, default='L')
    tags = TaggableManager()

    objects = QuestionManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    @ property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)

        return qs

    def get_absolute_url(self):
        return reverse("support:detail", kwargs={"slug": self.slug})

    _metadata = {
        'title': 'name',
        'content': 'abstract',

    }


@ receiver(post_save, sender=Question)
def blog_post_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        random_num = random.randint(1, 3910209312)
        instance.slug = slugify(instance.title)+'-'+str(random_num)
        instance.save()


class QuestionComment(models.Model):

    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=2000)

    # post    = models.ForeignKey(Post, blank=True, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(
        auto_now=False, auto_now_add=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True,
                               on_delete=models.CASCADE, related_name='comment_ques_parent')
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        # try:
        #     ques_obj = get_object_or_404(Question, id=self.object_id)
        # except:
        #     ques_obj = None
        return f'{self.user} commented {self.content}'

    # def children(self):
    #     return QuestionComment.objects.filter(parent=self)

    # @property
    # def is_parent(self):
    #     if self.parent is not None:
    #         return False
    #     return True


class Answer(models.Model):
    comment = models.ForeignKey(Comment, blank=True, null=True,
                                on_delete=models.SET_NULL, related_name='answer_comment')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answer_question')
    verified = models.BooleanField(default=False)
    date_posted = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.title


class BusinessType(models.Model):
    BUSINESS_CHOICE = [('question', 'Question'),
                       ('training', 'Training'), ('challenge', 'Challenge'), ]
    business = models.CharField(
        max_length=100, choices=BUSINESS_CHOICE)
    created = models.DateTimeField(
        auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business


class Order(models.Model):
    payment_id = models.CharField(max_length=1000)
    payment_email = models.EmailField()
    question = models.ForeignKey(
        Question, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.payment_id) + ' ' + str(self.question)


class PointsLookup(models.Model):

    TICKET_TYPE_CHOICES = [('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'),
                           ('Urgent', 'Urgent')
                           ]
    ticket_type = models.CharField(
        max_length=20, choices=TICKET_TYPE_CHOICES, blank=True, null=True)
    verified = models.BooleanField(default=False)
    vote_count = models.IntegerField(default=0)
    points = models.IntegerField()

    def __str__(self):
        return self.ticket_type+' '+str(self.verified)


class ReplyNotification(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author', blank=True, null=True)
    replied_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='replied_user', blank=True, null=True)
    commented_on = models.CharField(max_length=2000, blank=True, null=True)
    subject = models.CharField(max_length=2000, blank=True, null=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.user)
