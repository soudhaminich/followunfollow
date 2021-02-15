import base64
from django.urls import reverse
import uuid
from .models import FileTest
from .models import FileItem
from .config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, authentication
import time
import os
import hmac
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Favorite
from django.views.generic import View, ListView, TemplateView, DetailView, CreateView, FormView, UpdateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import PostCreationForm,PostUpdateForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, Http404
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.forms import CommentForm
from comments.models import Comment, Reply
from .tasks import s3_upload
from django.contrib import messages

import boto3
import json
from botocore.exceptions import ClientError
from botocore.client import Config

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from analytics.mixins import ObjectViewedMixin
from meta.views import Meta
from notifications.models import Notification
from support.models import Question, ReplyNotification
from taggit.models import Tag
from tecsee.models import TecseeVideo

def users_notification(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    user_unread_message = user.notifications.unread()
    object_notify = Notification.objects.filter(
        recipient=request.user, unread=True)
    ques = []
    for obj in object_notify:
        instance = Question.objects.get(id=obj.target_object_id)
        if instance is not None:
            ques.append(instance.slug)
    output = zip(object_notify, ques)
    context['object_notify'] = object_notify
    context['ques'] = ques
    context['user_unread_message'] = user_unread_message
    context['output'] = output
    # content_type = ContentType.objects.get_for_model(object_notify.target_content_type)
    # print(content_type)
    # user_obj = User.objects.get(id=request.user.id)
    # print(user_obj.notifications)
    # notification_count = user_obj.notifications.unread().count()
    return render(request, 'blogs/notification.html', context)
    # return JsonResponse(context)


def test(request):
    return render(request, 'blogs/test.html', {})


class BlogView(ListView):
    template_name = 'blogs/home.html'
    # queryset = Post.objects.filter(approved='Y')
    # ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(approved='Y').order_by('-date_posted')
        tag_slug = None
        if self.kwargs.get('tag_slug'):
            tag_slug = self.kwargs['tag_slug']
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        # print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
            video_list = TecseeVideo.objects.filter(approved='Y').first()
            context['video_list'] = video_list
        # print(context)
        return context

    def get(self, request, *args, **kwargs):
        # print(kwargs)
        # tag_slug = kwargs['tag_slug']
        # tag = None
        # if tag_slug:
        #     tag = get_object_or_404(Tag, slug=tag_slug)
        #     queryset = self.queryset.filter(tags__in=[tag])

        # either
        # print(request.get_raw_uri())
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect('support:question')
        return super().get(request, *args, **kwargs)

# ObjectViewedMixin


class BlogDetailView(ObjectViewedMixin, DetailView):
    # model = Post
    template_name = 'blogs/blog_detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        # print(request.session)
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Post, slug=slug)
        # instance = Post.objects.get_by_post_id(slug)

        if instance is None:
            raise Http404("sdfdsfds")
        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # favorite = Favorite.objects.filter(add_favorite=True)
        form = CommentForm(self.request.POST or None)
        slug = self.kwargs['slug']
        obj_post = Post.objects.get_by_post_id(slug)
        key = f'{obj_post.path}'
        # print(key)
        print(obj_post.blog_image.url)
        try:
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_S3_REGION_NAME)
            url = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                    'Key': key},
                                            )
            # temporary_fix = 'https://'+str(settings.AWS_S3_ENDPOINT_URL) +'/'+ str(key)
            # print(temporary_fix)
            context['new_url'] = url
            # print(url)
            # print(context)
        except Exception as e:
            print("An error occured", e)

        # instance = Post.objects.get_by_post_id(self.slug)
        # key = f'{instance.path}/{instance.video_file_name}'

        context['form'] = form
        # favorite    = Favorite.objects.all()
        # context['favorite'] =  favorite
        slug = self.kwargs['slug']
        # print(slug)
        content_type = ContentType.objects.get_for_model(Post)
        obj_id = obj_post.id
        # comment_obj = Comment.objects.filter(post__slug=slug)
        # comment_obj = Comment.objects.filter(content_type=content_type, object_id=obj_id)
        comment_obj = obj_post.comments
        # print(comment_obj)
        # reply_obj  = Reply.objects.filter(comment__post__slug=slug)
        reply_obj = Reply.objects.filter(comment__object_id=obj_id)
        comment_obj_count = comment_obj.count()
        # print(comment_obj_count)
        # related_posts = Post.objects.exclude(blog_image__isnull=True)
        # for i in related_posts:
        #     print(i.blog_image)
        # print(related_posts)

        # object_notify = Notification.objects.filter(recipient=self.request.user.id).exclude(unread=False)
        # print(object_notify)
        # quest_obj = Question.objects.get(id=15)
        # print(quest_obj)
        # user_obj = User.objects.get(id=self.request.user.id)
        # print(user_obj.notifications)
        # notification_count = user_obj.notifications.unread().count()
        # nty_cnt_str = ""
        # if notification_count > 0:
        #     nty_cnt_str = '('+str(user_obj.notifications.unread().count())+')'+' '
        from django.utils.html import strip_tags
        meta = Meta(
            # title="Teciky - Place for Techions",
            title=obj_post.title,
            image='https://static.teckiy.com/teckiy_logo_fav.jpg',
            description=strip_tags(obj_post.content),
            url=self.request.build_absolute_uri(),
            author="Teckiy",
            use_title_tag=True,
            use_facebook=True,
            use_og=True,
            fb=2529807007335836,
            type='website',
            keywords=['python', 'django', 'developer', 'support'],
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        context['meta'] = meta
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
        related_posts = Post.get_post_blog_image(Post)

        context['comment_obj'] = comment_obj
        context['comment_obj_count'] = comment_obj_count
        context['related_posts'] = related_posts
        context['reply_obj'] = reply_obj
        # context['user_obj'] = user_obj
        # context['object_notify'] = object_notify
        # context['quest_obj'] = quest_obj

        # print(context['comment_obj'])
        # print(context)
        return context


class AboutView(TemplateView):
    template_name = 'blogs/about.html'


class PolicyView(TemplateView):
    template_name = 'blogs/policy.html'


def about(request):
    return render(request, 'blogs/about.html', {})


def blog_delete_post(request, post_id):
    query = get_object_or_404(Post, pk=post_id)
    query.delete()
    return redirect('blogs:blog-home')


def create_post_form(request):
    pass
# class CreatePostView(CreateView):

#     form_class = PostCreationForm

#     success_url = reverse_lazy('blogs:blog-home')
#     template_name = 'blogs/create-post.html'


@login_required
def delete_blog_post(request, slug):
    query = get_object_or_404(Post, slug=slug)
    if request.user == query.author:
        query.delete()
        messages.success(request, 'Post has been successfully removed !!!')
        return redirect('blogs:blog-home')
    else:
        messages.success(
            request, 'Sorry! You dont have access to delete this post!!!')
        return redirect('blogs:blog-home')


class CreatePostView(SuccessMessageMixin, CreateView):

    form_class = PostCreationForm
    # model = Post

    # fields = ['title', 'content', 'blog_image', 'tags']
    # success_url = reverse_lazy('blogs:blog-home')
    template_name = 'blogs/post_create.html'
    success_message = "Your Post has been submited for review !!!"

    # def form_valid(self, form):
    #     photo_file = request.FILES['upload-file']
    #     print(request.POST)

    #     if photo_file:
    #         s3 = boto3.client('s3', aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID, aws_secret_access_key=AWS_UPLOAD_SECRET_KEY,
    #                           region_name=AWS_UPLOAD_REGION)
    #         try:
    #             key = uuid.uuid4().hex[:6] + \
    #                 photo_file.name[photo_file.name.rfind('.'):]
    #             mimetype = 'video/mp4'
    #             s3.upload_fileobj(photo_file, AWS_UPLOAD_BUCKET, key,
    #                               ExtraArgs={
    #                                   "ContentType": mimetype
    #                               })
    #             url = s3.generate_presigned_url('get_object',
    #                                             Params={'Bucket': AWS_UPLOAD_BUCKET,
    #                                                     'Key': key},
    #                                             )

    #             upload_url = FileTest(file_test=url, user_id=self.request.user.id)
    #             upload_url.save()
    #         except Exception as e:
    #             print("An error to s3", e)
    #     form.instance.author = self.request.user
    #     subject = f'{form.instance.author} posted new {form.instance.title}'
    #     body = f'''Hi {form.instance.author}, \n
    #                    Please reach out to info@virtual2buy.com for any issues !!!\n
    #                    Regards,
    #                    {settings.PROJECT_TITLE} Blog Team
    #                 '''
    #     # sleepy.delay(10)
    #     send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [
    #               self.request.user.email], fail_silently=False)
    #     return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     context = {'form': PostCreationForm()}
    #     return render(request, 'blogs/post_create.html', context)

    # def post(self, request, *args, **kwargs):
    #     form = PostCreationForm(request.POST)
    #     if form.is_valid():
    #         post = form.save()
    #         post.save()
    #         return HttpResponseRedirect(reverse_lazy('blogs:blog-home', args=[request.POST.user]))
    #     return render(request, 'blogs/post_create.html', {'form': form})
    def get_success_url(self):
        # print(self.object.priority)
        if self.object.publish and self.object.approved == 'N':
            self.success_message = "Your Blog has been successfully submitted for Techions review. We will let you know once its approved.!!!"
            return reverse('blogs:blog-home')
        elif not self.object.publish and self.object.draft:
            self.success_message = "Your Blog has been successfully saved!!!"
            return reverse('blogs:blog-home')
        elif self.object.publish and self.object.approved == 'Y':
            self.success_message = "Your Blog has been successfully updated!!!"
            return reverse('blogs:blog-home')
        # elif self.object.author != request.user:
        #     self.success_message = "You may not have permission to view this page!!!"
        #     return reverse('blogs:blog-home')
        return reverse('blogs:blog-home')
        # return reverse('support:detail', args=(self.object.slug,))

    def form_valid(self, form):
        # print(self.request.POST.get('draft'))
        if self.request.POST.get('draft') == 'Save Draft':
            success_message = "Your Post has been saved!!!"
            form.instance.author = self.request.user
            form.instance.draft = True
            return super(CreatePostView, self).form_valid(form)
        else:
            form.instance.author = self.request.user
            form.instance.publish = True
            return super(CreatePostView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
        return context


class UpdatePost(UpdateView):
    # form_class = PostCreationForm
    form_class = PostUpdateForm
    model = Post
    # fields = ['title', 'content', 'blog_image', 'tags']
    template_name = 'blogs/post_create.html'
    # template_name_suffix = 'PostCreationForm'

# class UpdatePost(CreateUpdatePostView, UpdateView):
#     def get_queryset(self):
#         base_qs = super(UpdatePost, self).get_queryset()
#         return base_qs.filter(author=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super(UpdatePost, self).get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             notify_list = ReplyNotification.objects.filter(
#                 user=self.request.user).distinct()
#             notify_list.update(read=True)
#             context['notify_list'] = notify_list
#         return context

    # def get_success_url(self):
    #     if self.request.user != self.object.author:
    #         self.success_message = "You may not have permission to view this page!!!"
    #         return reverse('blogs:blog-home')


def ajax_request(request):
    user = request.user
    data = {
        'user': user
    }

    return JsonResponse(data)


class CreateCrudUser(View):
    def get(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.create(
            name=name1,
            address=address1,
            age=age1
        )

        user = {'id': obj.id, 'name': obj.name,
                'address': obj.address, 'age': obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)


class BlogUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content', ]
    template_name = 'blogs/post_update.html'
    # success_url = reverse_lazy('blogs:blog-home')
    success_message = "Your Post has been updated!!!"

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = Post.objects.get_by_post_id(slug)
        if instance is None:
            raise Http404("Blog doesn't exist")
        return instance

    def get_success_url(self):
        return reverse('blogs:detail', kwargs={'slug': self.object.slug})


def favorite_like(request, post_id=None, fav_id=None):
    print(fav_id)
    if fav_id == '0':
        # print(fav_id)
        user = User.objects.get(username__iexact=request.user)
        post = Post.objects.get(id=post_id)
        # print(post)
        obj = Favorite.objects.create(
            user=user,
            add_favorite=True,
            post=post
        )
        return redirect('blogs:blog-home')
        # data = {
        #     'color' : 'red',
        #     'obj': obj.id,
        #     'url': f'/blogs/favorite/{obj.post.id}/{obj.id}'
        #     }
        # return JsonResponse(data)

    else:
        # Delete
        print('Tets', fav_id)
        instance = Favorite.objects.filter(id=fav_id)
        instance.delete()
        return redirect('blogs:blog-home')

    data = {

    }
    # return redirect('blogs:blog-home')
    return JsonResponse(data)


def ajax_like(request, post_id=None, fav_id=None):
    if fav_id == '0':

        user = User.objects.get(username__iexact=request.user)
        post = Post.objects.get(id=post_id)
        obj = Favorite.objects.create(
            user=user,
            add_favorite=True,
            post=post
        )
        data = {
            'color': 'red',
            'obj': obj.id,
            'url': f'/ajax/{obj.post.id}/{obj.id}'
        }
        print('created')
        return JsonResponse(data)
    else:
        print(fav_id)
        instance = Favorite.objects.filter(id=fav_id)
        instance.delete()
        print('Deleted')
        data = {
            'color': 'black',
            'url': f'/ajax/{post_id}/0'
        }
        return JsonResponse(data)

    return True
# def ajax_like(request, post_id=None, fav_id=None):
#     print(fav_id)
#     if fav_id == '0':
#         # print(fav_id)
#         user = User.objects.get(username__iexact=request.user)
#         post = Post.objects.get(id=post_id)

#         #check if exists or not

#         try:   # fav_instance = Favorite.objects.filter(user=user, post=post)
#             fav_instance = get_object_or_404(Favorite, user=user, post=post)

#             print(fav_instance)
#             fav_instance.user = user
#             fav_instance.post = post
#             fav_instance.add_favorite = True
#             fav_instance.save()

#             # instance.save()
#             # print(instance)
#             # print(f'/blogs/ajax/{instance.post.id}/{instance.id}')

#             print('Updated...')
#             print(f'/blogs/ajax/{post_id}/{fav_instance.fav_id}')

#             data = {
#                 'color' : 'red',
#                 'url': f'/blogs/ajax/{post_id}/{fav_instance.fav_id}'
#                 }
#             return JsonResponse(data)
#         except Exception as e:
#             print(post)
#             obj = Favorite.objects.create(
#                             user=user,
#                             add_favorite=True,
#                             post=post
#                             )

#             # return redirect('blogs:blog-home')
#             data = {
#                 'color' : 'red',
#                 'obj': obj.id,
#                 'url': f'/blogs/ajax/{obj.post.id}/{obj.id}'
#                 }
#             return JsonResponse(data)

#     else:
#         #Delete
#         print('Test', fav_id)
#         instance = get_object_or_404(Favorite, id=fav_id)
#         # instance = Favorite.objects.filter(id=fav_id)
#         instance.delete()
#         print('Deleted')

#         if instance.add_favorite == True:
#             # instance.delete()
#             # print('Deleted')
#             print(True)
#             user = User.objects.get(username__iexact=request.user)
#             post = Post.objects.get(id=post_id)
#         # print(instance)


#             # obj, created = Favorite.objects.update(
#             #     user=user,
#             #     add_favorite=False,
#             #     post=post
#             #     )
#             instance.user = user
#             instance.post = post
#             instance.add_favorite = False
#             instance.save()


#             # instance.save()
#             # print(instance)
#             # print(f'/blogs/ajax/{instance.post.id}/{instance.id}')

#             print('Updated False')
#             print(f'/blogs/ajax/{post_id}/{fav_id}')

#             data = {
#                 'color' : 'black',
#                 'url': f'/blogs/ajax/{post_id}/{fav_id}'
#                 }
#             return JsonResponse(data)
#         elif instance.add_favorite == False:
#                         # instance.delete()
#             # print('Deleted')
#             print(False)
#             user = User.objects.get(username__iexact=request.user)
#             post = Post.objects.get(id=post_id)
#         # print(instance)


#             # obj, created = Favorite.objects.update(
#             #     user=user,
#             #     add_favorite=False,
#             #     post=post
#             #     )
#             instance.user = user
#             instance.post = post
#             instance.add_favorite = True
#             instance.save()

#             # instance.save()
#             # print(instance)
#             # print(f'/blogs/ajax/{instance.post.id}/{instance.id}')

#             print('Updated')
#             print(f'/blogs/ajax/{post_id}/{fav_id}')

#             data = {
#                 'color' : 'red',
#                 'url': f'/blogs/ajax/{post_id}/{fav_id}'
#                 }
#             return JsonResponse(data)
#         else:
#             user = User.objects.get(username__iexact=request.user)
#             post = Post.objects.get(id=post_id)
#             obj = Favorite.objects.create(
#                             user=user,
#                             add_favorite=True,
#                             post=post
#                             )
#             data = {
#                 'color' : 'red',
#                 'obj': obj.id,
#                 'url': f'/blogs/ajax/{obj.post.id}/{obj.id}'
#                 }
#             return JsonResponse(data)

def upload_test(request):
    return render(request, 'blogs/upload.html', {})


@login_required
def create_post(request):
    form = PostCreationForm()
    return render(request, 'blogs/post_new_create.html', {'form': form})


class FilePolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a FileItem object instance in our
    Django backend. This is to include the FileItem instance in the path
    we will use within our bucket as you'll see below.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        """
        The initial post request includes the filename
        and auth credientails. In our case, we'll use
        Session Authentication but any auth should work.
        """
        print(request)
        filename_req = request.data.get('filename')
        print(filename_req)
        unique_key = uuid.uuid4().hex[:6]
        file_name = filename_req[:filename_req.rfind('.')]
        file_extension = filename_req[filename_req.rfind('.'):]
        print(file_name, file_extension)
        file_name_replace = file_name.replace(" ", "_")
        title = request.data.get('title')
        content = request.data.get('content')

        # new_file_name = file_name.replace(" ","_")
        # orig_final_name = str(photo_file).replace(" ","_")
        # print(new_file_name,orig_final_name)
        # print(content)
        if not filename_req:
            return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        policy_expires = int(time.time()+(24 * 60 * 60 * 1000))
        user = request.user
        # print(user)
        username_str = str(request.user.username)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS. 

        Example:
        To-be-uploaded file's name: Some Random File.mp4
        Eventual Path on S3: <bucket>/username/2312/2312.mp4
        """
        # file_obj = FileItem.objects.create(user=user, name=filename_req)
        orig_final_name = str(filename_req).replace(" ", "_")
        post_obj = Post(author=user, video_file_name=orig_final_name, title=title, content=content,
                        file_type=file_extension)
        post_obj.save()
        file_obj_id = post_obj.id
        upload_start_path = "{username}/{file_obj_id}/".format(
            username=username_str,
            file_obj_id=file_obj_id

        )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
            file_obj_id=file_obj_id,
            file_extension=file_extension

        )
        """
        Eventual file_upload_path includes the renamed file to the 
        Django-stored FileItem instance ID. Renaming the file is 
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
            upload_start_path=upload_start_path,
            filename_final=filename_final,
        )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-stored FileItem instance
            """
            # file_obj.path = final_upload_path
            post_obj.path = final_upload_path
            # file_obj.save()
            post_obj.save()

        policy_document_context = {
            "expire": policy_expires,
            "bucket_name": settings.AWS_STORAGE_BUCKET_NAME,
            "key_name": "",
            "acl_name": "private",
            "content_name": "",
            "content_length": 524288000,

            "upload_start_path": upload_start_path,

        }
        policy_document = """
        {"expiration": "2020-12-31T00:00:00Z",
          "conditions": [ 
            {"bucket": "%(bucket_name)s"}, 
            ["starts-with", "$key", "%(upload_start_path)s"],
            {"acl": "%(acl_name)s"},
            
            ["starts-with", "$Content-Type", "%(content_name)s"],
            ["starts-with", "$filename", ""],
            ["content-length-range", 0, %(content_length)d]
          ]
        }
        """ % policy_document_context
        aws_secret = str.encode(settings.AWS_SECRET_ACCESS_KEY)
        policy_document_str_encoded = str.encode(
            policy_document.replace(" ", ""))
        url = 'https://{bucket}.s3-{region}.amazonaws.com/'.format(
            bucket=settings.AWS_STORAGE_BUCKET_NAME,
            region=settings.AWS_S3_REGION_NAME
        )
        policy = base64.b64encode(policy_document_str_encoded)
        signature = base64.b64encode(
            hmac.new(aws_secret, policy, hashlib.sha1).digest())
        data = {
            "policy": policy,
            "signature": signature,
            "key": settings.AWS_ACCESS_KEY_ID,
            "file_bucket_path": upload_start_path,
            "file_id": file_obj_id,
            "filename": filename_final,
            "url": url,

            "username": username_str,
        }
        return Response(data, status=status.HTTP_200_OK)


class FileUploadCompleteHandler(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        print(request.data)
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        data = {}
        type_ = request.POST.get('fileType')
        if file_id:
            obj = Post.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = True
            # obj.type = type_
            obj.save()
            data['id'] = obj.id
            data['saved'] = True
        return Response(data, status=status.HTTP_200_OK)


def sign_s3(request, file_name):
    S3_BUCKET = AWS_UPLOAD_BUCKET
    print(request.GET)
    print(file_name)
    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')
    print(file_type)
    s3 = boto3.client('s3', 'us-east-2', aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID, aws_secret_access_key=AWS_UPLOAD_SECRET_KEY
                      )
    print(s3)
    try:
        presigned_post = s3.generate_presigned_post(

            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type}
            ],

            ExpiresIn=604800
        )
        updated_url = 'https://django-s3-letslearntech.s3-us-west-2.amazonaws.com/{0}'.format(
            file_name)
        # print(updated_url)

        print(presigned_post)
        output = {
            'data': presigned_post
        }

        return JsonResponse({
            'data': presigned_post,
            # 'url': updated_url
        })
    except ClientError as e:
        logging.error(e)
        return None

    # return Response(data=presigned_post, status=status.HTTP_200_OK)
    # return json.dumps({
    # 'data': presigned_post,
    # 'url': 'https://{}.s3.amazonaws.com/{}'.format(S3_BUCKET, file_name)
    # })

# def create_story(request):
#     form = PostCreationForm()

#     if request.method == 'POST' and request.FILES['video_upload']:
#         print('hi')
#         username = request.user.username
#         photo_file = request.FILES['video_upload']
#         video_poster = request.FILES['video_poster']
#         print(video_poster)
#         unique_key = uuid.uuid4().hex[:6]
#         file_name = photo_file.name[:photo_file.name.rfind('.')]
#         # print(new_file_name.replace(" ", "_"))

#         file_type = photo_file.name[photo_file.name.rfind('.'):]
#         title = request.POST.get('title')
#         content = request.POST.get('content')

#         new_file_name = file_name.replace(" ","_")
#         orig_final_name = str(photo_file).replace(" ","_")

#         user = request.user
#         print(title,content)
#         new_post = Post(author=user, video_file_name=orig_final_name,title=title,content=content,
#                 file_type=file_type,video_poster=video_poster)
#         new_post.save()

#         key = "{username}/{file_obj_id}/{unique_key}/{orig_name}".format(
#                     username = username,
#                     file_obj_id = new_post.id,
#                     unique_key=unique_key,
#                     orig_name=orig_final_name
#             )
#         print(key)

#         if photo_file:
#             # s3_upload.delay(str(photo_file),key,new_post.id)
#             s3 = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#             region_name=settings.AWS_S3_REGION_NAME)
#             try:
#                 # key=uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#                 mimetype = 'video/mp4'
#                 s3.upload_fileobj(photo_file,settings.AWS_STORAGE_BUCKET_NAME,key,
#                                 ExtraArgs={
#                         "ContentType": mimetype
#                     })
#                 # url = s3.generate_presigned_url('get_object',
#                 #                                     Params={'Bucket': AWS_UPLOAD_BUCKET,
#                 #                                             'Key':key},
#                 #                                     )
#                 # url = f'https://django-s3-letslearntech.s3-us-west-2.amazonaws.com/{key}'
#                 # upload_url = FileTest(file_test=url,user_id=request.user.id)
#                 # upload_url.save()
#                 # print(url)
#                 update_create_post = Post.objects.filter(id=new_post.id).update(path=key,uploaded = True)
#                 # messages.success(request,('Post has been submmitted for review.'))
#                 # return redirect('blogs:blog-home')
#                 return JsonResponse({"nothing to see": "this isn't happening"})
#             except Exception as e:
#                 return JsonResponse({"nothing to see": "failed"})

#     # obj = FileTest.objects.all()
#     return render(request,'blogs/post_create.html',{'form': form})


@login_required
def create_story(request):

    form = PostCreationForm()

    response = {}
    if request.method == 'POST':
        print(request.POST.get('title'))
        messages.success(request, ('Post has been submmitted for review.'))
        return redirect('blogs:blog-home')

    # obj = FileTest.objects.all()
    return render(request, 'blogs/post_create.html', {'form': form})


def donate(request):
    return render(request, 'blogs/sponsors.html', {})


def handler500(request):
    return render(request, '500.html', status=500)
