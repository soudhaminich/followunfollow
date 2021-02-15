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
from comments.models import Comment

# Create your models here.


def validate_image(instance):
    print(instance)
    # image = self.cleaned_data['image']
    # print(image)
    # print(image.size)
    file_size = instance.size
    limit_kb = 150
    ext = os.path.splitext(instance.name)[1]
    valid_extensions = ['.jpg', '.png']
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    return instance


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
    return "profile_pics/{author_name}/{file_name}_{final_filename}".format(
        final_filename=final_filename,
        author_name=instance.user,
        file_name=name
    )


def validate_file(file):
    print(file)
    file_size = file.size
    limit_kb = 150
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.jpg', '.png']
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class ProfileManager(models.Manager):

    def get_techion(self):
        qs = super(ProfileManager, self).filter(techion=True)
        return qs


class Profile(models.Model):
    # SKILL_CHOICE = [('P','Python'),('D','Django'),('S','SQL'),('Or','Oracle'),('JS','Javascript'),('O','Other')]
    BADGE_CHOICES = [('SME', 'Teckiy SME'), ('bronze', 'Bronze'),
                     ('silver', 'Silver'), ('gold', 'Gold')]
    INTERESTED_CHOICES = [('active', 'Actively looking job right now'), ('freelancer', 'Freelancer'),
                          ('lerning', 'Learning')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default='default.jpg', upload_to=upload_image_path, validators=[validate_file])
    image = models.ImageField(default='default.jpg',
                              upload_to=upload_image_path, validators=[validate_image])
    display_name = models.CharField(
        max_length=30, null=True, unique=True)
    dob = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    professional_summary = RichTextUploadingField(
        config_name='profile_ckeditor', blank=True, null=True)
    skillset = models.CharField(max_length=1000, blank=True, null=True)
    techion = models.BooleanField(default=False)
    slug = models.SlugField(max_length=2000, blank=True, null=True)
    amount_opt_in = models.BooleanField(default=False)
    fb_url = models.URLField(blank=True, null=True)
    tw_url = models.URLField(blank=True, null=True)
    lki_url = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    paypal_account = models.EmailField(null=True, blank=True)
    badges = models.CharField(
        max_length=200, choices=BADGE_CHOICES, blank=True, null=True)
    preferences = models.CharField(
        max_length=200, choices=INTERESTED_CHOICES, blank=True, null=True)
    following=models.ManyToManyField(User,related_name='following',blank=True)
    # first_name = models.CharField
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username} account profile'

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"slug": self.slug})

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


@receiver(post_save, sender=Profile)
def profile_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.slug is None:
        instance.slug = instance.user.username
        instance.save()


# class TechionProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     badges = models.CharField(max_length=200, blank=True, null=True)
#     points = models.IntegerField(blank=True, null=True)
#     ticket = models.ForeignKey(
#         Question, blank=True, null=True, on_delete=models.SET_NULL)
#     paypal_account = models.EmailField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username


class UserFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, related_name='Profilefollowing', on_delete=models.SET_NULL, blank=True, null=True)
    following = models.ForeignKey(
        User, related_name='followers',  on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


class UserActionManager(models.Manager):

    def upvote_count(self):
        qs = super(UserActionManager, self).filter(vote_type='U')
        return qs.count()

    def downvote_count(self):
        qs = super(UserActionManager, self).filter(vote_type='D')
        return qs.count()


class UserAction(models.Model):
    VOTE_UP = 'U'
    VOTE_DOWN = 'D'
    PRIORITY_URGENT_PENDING = 'UP'
    VOTE_TYPE_CHOICES = [(VOTE_UP, 'Up'), (VOTE_DOWN, 'Down'),
                         ]
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name='users')
    vote = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    vote_type = models.CharField(
        max_length=20, choices=VOTE_TYPE_CHOICES, blank=True, null=True)

    objects = UserActionManager()

    class Meta:
        unique_together = [('comment', 'user',)]

    def __str__(self):
        return self.user.username

    @property
    def upvote(self):
        return self.vote_type


class Techion(models.Model):
    profile = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name='profiles')
    points = models.IntegerField(default=0)
    redeem_points = models.IntegerField(default=0)
    ticket = models.ForeignKey(
        Question, blank=True, null=True, on_delete=models.SET_NULL, related_name='tickets')
    vote_count = models.IntegerField(default=0)
    created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.profile.user.username) + ' ' + str(self.ticket.title)
