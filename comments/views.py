from django.contrib import messages
from django.urls import reverse
import json
from django.shortcuts import render, redirect
from .models import Comment, Reply
from .forms import CommentForm
from django.http import JsonResponse, HttpResponse, Http404
from blogs.models import Post
# Create your views here.
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from support.models import Question, ReplyNotification
from tecsee.models import TecseeVideo
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.sites.models import Site
from .tasks import comment_send
from django.template.loader import render_to_string

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ConfirmNotification(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse('OK')
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(ConfirmNotification, self).dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     body = json.loads(request.body)
    #     ReplyNotification.objects.filter(
    #         pk=body['notification_id'], user=request.user
    #     ).delete()
    #     return HttpResponse('OK')


def save_notification(question=None, comment=None, reply_text=None, author=None,
                      replied_user=None, commented_on=None,
                      subject=None):
    notification = ReplyNotification()
    if question:
        notification.question = question
        notification.user = question.user
        notification.author = author
        notification.replied_user = replied_user
        notification.commented_on = commented_on
        notification.subject = subject

    if comment:
        notification.comment = comment
        notification.user = comment.user
        notification.author = author
        notification.replied_user = replied_user
        notification.commented_on = commented_on
        notification.subject = subject
    notification.save()
    # print('Question notification alert ', question, comment)
    channel_layer = get_channel_layer()
    # data = serializers.serialize('json', [notification.comment, ])

    # data = 'hi'

    # notify_count = ReplyNotification.objects.filter(
    #     pk=notification.pk).count()
    notify_count = 0
    for out in ReplyNotification.objects.filter(
            user=notification.user):
        if out.question:
            if out.user == out.author:
                notify_count += 1
        else:
            if out.user != out.author:
                notify_count += 1

    # notify_count = ReplyNotification.objects.filter(
    #     user_id=notification.user).count()
    user_count = 0
    # for out in ReplyNotification.objects.filter(
    #         user=request.user):
    #     if out.question:
    #         if out.user == out.author:
    #             user_count += 1
    #     else:
    #         if out.user != out.author:
    #             user_count += 1
    # print(user_count)
    data = notify_count + user_count
    # data = notification.comment.comment
    # Trigger message sent to user
    async_to_sync(channel_layer.group_send)(
        str(notification.user.pk),  # Group Name, Should always be string
        {
            "type": "notify",   # Custom Function written in the channels.py
            "text": data,
            "notification_id": notification.pk
        },
    )


@login_required
def comment_view(request, post_id=None):
    # print(request.method)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # print(form)
        print('Is it working')
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = request.POST['parent_id']
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()
            instance = form.save(commit=False)
            instance.user = request.user  # Set the user object here
            post_instance = Post.objects.get(id=post_id)
            instance.content_type = ContentType.objects.get_for_model(Post)
            instance.object_id = post_instance.id
            instance.parent = parent_obj
            # instance.post = post_instance
            instance.save()

            # instance = Comment.objects.all().order_by("-id")[0]
            # print(instance)
            comment_slug = Post.objects.get_by_post_id(post_instance.slug)
            # comment_slug = Post.objects.filter(id=post_id)
            return redirect('blogs:detail', comment_slug.slug)
    #         data = {
    #             'color' : 'red',
    #             'comment_msg': instance.comment
    #             }

    #         return JsonResponse(data)
    #     data = {
    #         'color' : 'red'
    #         }
    #     return JsonResponse(data)
    #     # return HttpResponseRedirect(reverse('blogs:detail', args=[1]))
    # else:
    #     form = CommentForm()
    #     data = {
    #         'color' : 'red'
    #         }
    #     return JsonResponse(data)
    return redirect('blogs:blog-home')


@login_required
def reply_question_edit(request, object_id=None, reply_id=None):
    print(request.POST['reply_id'])
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            upd_comment = request.POST['comment']
            reply_id = request.POST.get('reply_id', None)
            print('reply', reply_id)
            parent_id = request.POST['parent_id']
            # print(reply_id)
            if reply_id == "":
                reply_id = None
            if reply_id is not None:
                print('testing')
                reply_qs = Comment.objects.get(id=reply_id)
                reply_qs.comment = upd_comment
                reply_qs.save()
                comment_slug = Question.objects.get(
                    id=object_id)

                return redirect('support:detail', comment_slug.slug)
            else:
                comment_qs = Comment.objects.get(id=parent_id)
                comment_qs.comment = upd_comment
                comment_qs.save()
                comment_slug = Question.objects.get(
                    id=object_id)

                return redirect('support:detail', comment_slug.slug)
        else:
            question_instance = Question.objects.get(id=object_id)            
            messages.error(request, 'Update should not be empty!')
            return redirect('support:detail', question_instance.slug)

    return redirect('support:question')


@login_required
def comment_question_view(request, object_id=None):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = request.POST['parent_id']
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()
            instance = form.save(commit=False)
            instance.user = request.user  # Set the user object here
            question_instance = Question.objects.get(id=object_id)
            if question_instance.status == 'O':
                question_instance.status = 'I'
                question_instance.save()
            instance.content_type = ContentType.objects.get_for_model(Question)
            instance.object_id = question_instance.id
            instance.parent = parent_obj
            instance.save()
            # from notifications.signals import notify
            # # if request.user != question_instance.user:
            # notify.send(request.user,
            #             recipient=question_instance.user,
            #             verb=instance.comment,
            #             target=question_instance)
            comment_slug = Question.objects.get_by_question_id(
                question_instance.slug)
            commented_user = request.user.username
            question_user_email = comment_slug.user.email
            question_url = comment_slug.get_absolute_url()
            question_title = comment_slug.title
            ticket_id = comment_slug.id
            subject = f'Teckiy New message from {commented_user} -   {question_title} #Ticket{ticket_id}'

            # body    = f'''Hi Teckiy,
            #                 Someone response to your question. Please check.
            #                 Thanks,
            #                 Teckiy Team
            #                 https://www.teckiy.com
            #                 !!!
            #             '''
            email = question_user_email
            bcc_email = settings.ADMIN_EMAIL
            # print(email,bcc_email)
            # print('email', email)
            if settings.DEBUG:
                domain = 'http://localhost:8000'
            else:
                domain = 'https://www.teckiy.com'

            text_content = 'This is an important message.'
            html_content = render_to_string(
                'support/question_email.html', {'commented_user': commented_user,
                                                'domain': domain, 'question_url': question_url, 'to_user': comment_slug.user.username})
            # html_content = f"""
            #                     <html>
            #                     <body>
            #                     <br/>
            #                     <p>Hi Teckiy, <br/>
            #                         <strong>{commented_user}</strong>
            #                              has responded to your question,
            #                             <br/>
            #                             <a href="{domain}{question_url}">click here</a>
            #                             <br/>
            #                         Thanks,<br/>
            #                         Teckiy Team<br/>
            #                         https://www.teckiy.com
            #                         <br/>

            #                     </p>
            #                     </body>
            #                     </html>
            #                 """
            # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,[obj.email],fail_silently=False)
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email],
                                         bcc=[bcc_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            if not instance.user.profile.paypal_account:
                messages.info(
                    request,
                    'Please fill your <a href="{}">paypal account</a> to redeem your points($)'.
                    format(reverse('users:profile', kwargs={
                           'username': instance.user.username})),
                    extra_tags='safe'
                )
            users = []
            if instance.user != question_instance.user:
                users.append(instance.user)
                save_notification(question=question_instance,
                                  reply_text=instance, author=question_instance.user, replied_user=instance.user,
                                  commented_on=question_instance.slug, subject=question_instance.title)
            # print('first instance user ', users)
            # print('question instance user ',  question_instance.user)
            for r in question_instance.comments.exclude(user=instance.user):
                # print(r.user)
                if r.user not in users:
                    users.append(r.user)
                    save_notification(comment=r, reply_text=instance.comment,
                                      author=question_instance.user, replied_user=instance.user,
                                      commented_on=question_instance.slug, subject=question_instance.title)
            return redirect('support:detail', comment_slug.slug)
        else:
            question_instance = Question.objects.get(id=object_id)            
            messages.error(request, 'Answer should not be empty!')
            return redirect('support:detail', question_instance.slug)
    return redirect('support:question')


def comment_test_json(request, post_id=None):
    print(request.POST)
    data = {}
    # print(request.is_ajax())
    if request.user:
        if request.method == 'POST':
            comment = request.POST['comment']
            post = Post.objects.get(id=post_id)
            new_comment_obj = Comment(
                comment=comment, user=request.user, post=post)
            new_comment_obj.save()

            data = new_comment_obj.serialize()
            # comment_slug = Post.objects.get(id=post.id)
            # comment_slug = Post.objects.filter(id=post_id)
            # return redirect('blogs:detail', comment_slug.slug)
            return JsonResponse(data)
            # return redirect('blogs:blog-home')
        else:

            qs = Comment.objects.filter(post=post_id)
            reply_qs = Reply.objects.filter(comment__post__id=post_id)
            # comment_obj = [
            #             {
            #                 "id":x.id,
            #                 "user": x.user.first_name,
            #                 "comment": x.comment,
            #                 'image':x.user.profile.image.url,
            #                 'updated_time': x.timestamp
            #             } for x in qs]
            comment_obj = [x.serialize() for x in qs]
            reply_obj = [x.serialize() for x in reply_qs]
            # print(comment_obj)
            # return HttpResponse('Welcome')
            data['reply_response'] = reply_obj
            print(data)
            if comment_obj is not None:
                data['response'] = comment_obj
            # print(data)
            return JsonResponse(data)
    data['error'] = 'User is not authenticated to comment'
    return JsonResponse(data)


def reply(request, post_id=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    reply = body['reply']
    post_id = body['post_id']
    print(post_id, reply)
    data = {}
    if request.method == 'POST':
        print('Post request')
        # comment = request.POST['comment']
        # comment = request.POST['comment']
        # post = Post.objects.get(id=post_id)
        # new_comment_obj = Comment(comment=comment,user=request.user,post=post)
        # new_comment_obj.save()
        # new_reply_obj = Reply(user=request.user,comment=new_comment_obj)
        # new_reply_obj.save()
        # data = new_comment_obj.serialize()
        # print(data)
        data['response'] = 'True'
        return JsonResponse(data)
    return JsonResponse({})


def reply_comment(request, comment_id, post_id):
    if request.method == 'POST':
        replied = request.POST['replied']
        comment_obj = Comment.objects.get(id=comment_id)
        new_reply_obj = Reply(
            user=request.user, replied=replied, comment=comment_obj)
        new_reply_obj.save()
        print(comment_obj)
        comment_slug = Post.objects.get(id=post_id)
        print(comment_slug)
        # comment_slug = Post.objects.filter(id=post_id)
        return redirect('blogs:detail', comment_slug.slug)
        # response = {}
        # response['content'] = new_reply_obj.serialize()
        # print(response)
        # return JsonResponse(response)
    return redirect('blogs:blog-home')


def comment_test(request, post_id=None):
    print(request.POST)
    data = {}
    # print(request.is_ajax())
    if request.user:
        if request.method == 'POST':
            comment = request.POST['comment']
            post = Post.objects.get(id=post_id)
            new_comment_obj = Comment(
                comment=comment, user=request.user, post=post)
            new_comment_obj.save()
            data = new_comment_obj.serialize()
            # comment_slug = Post.objects.get(id=post.id)
            comment_slug = Post.objects.filter(id=post_id)
            return redirect('blogs:detail', comment_slug.slug)
            # return JsonResponse(data)
            # return redirect('blogs:blog-home')
        else:

            qs = Comment.objects.filter(post=post_id)
            reply_qs = Reply.objects.filter(comment__post__id=post_id)
            # comment_obj = [
            #             {
            #                 "id":x.id,
            #                 "user": x.user.first_name,
            #                 "comment": x.comment,
            #                 'image':x.user.profile.image.url,
            #                 'updated_time': x.timestamp
            #             } for x in qs]
            comment_obj = [x.serialize() for x in qs]
            reply_obj = [x.serialize() for x in reply_qs]
            # print(comment_obj)
            # return HttpResponse('Welcome')
            data['reply_response'] = reply_obj
            print(data)
            if comment_obj is not None:
                data['response'] = comment_obj
            # print(data)
            return JsonResponse(data)
    data['error'] = 'User is not authenticated to comment'
    return JsonResponse(data)


def comment_list(request, *args, **kwargs):
    print('Its working')
    data = {
        'is_true': 'Yes'
    }
    return JsonResponse(data)


def comment_delete(request, comment_id=None, klass=None):
    if klass == 'question':
        try:

            delete_comment = Comment.objects.get(id=comment_id)

            question_instance = Question.objects.get(
                id=delete_comment.object_id)
            delete_comment.delete()
            data = {
                'deleted': 'Yes'
            }
            comment_slug = Question.objects.get_by_question_id(
                question_instance.slug)
            return redirect('support:detail', comment_slug.slug)
        except Exception as e:
            print(e)
    elif klass == 'video':
        try:

            delete_comment = Comment.objects.get(id=comment_id)

            tecsee_instance = TecseeVideo.objects.get(
                id=delete_comment.object_id)
            delete_comment.delete()
            data = {
                'deleted': 'Yes'
            }
            comment_slug = TecseeVideo.objects.get_by_tecsee_id(
                tecsee_instance.slug)
            return redirect('tecsee:detail', comment_slug.slug)
        except Exception as e:
            print(e)
    else:
        try:

            delete_comment = Comment.objects.get(id=comment_id)

            post_instance = Post.objects.get(id=delete_comment.object_id)
            delete_comment.delete()
            data = {
                'deleted': 'Yes'
            }
            comment_slug = Post.objects.get_by_post_id(post_instance.slug)
            return redirect('blogs:detail', comment_slug.slug)
        except Exception as e:
            print(e)

    return HttpResponse(comment_id)


def reply_delete(request, reply_id=None, klass=None):
    if klass == 'question':
        try:

            delete_reply = Comment.objects.get(id=reply_id)

            question_instance = Question.objects.get(id=delete_reply.object_id)
            delete_reply.delete()
            data = {
                'deleted': 'Yes'
            }
            comment_slug = Question.objects.get_by_question_id(
                question_instance.slug)
            return redirect('support:detail', comment_slug.slug)
        except Exception as e:
            print(e)
    elif klass == 'video':
        try:

            delete_reply = Comment.objects.get(id=reply_id)

            tecsee_instance = TecseeVideo.objects.get(id=delete_reply.object_id)
            delete_reply.delete()
            data = {
                'deleted': 'Yes'
            }
            comment_slug = TecseeVideo.objects.get_by_tecsee_id(
                tecsee_instance.slug)
            return redirect('tecsee:detail', comment_slug.slug)
        except Exception as e:
            print(e)
    else:
        try:

            delete_reply = Comment.objects.get(id=reply_id)

            post_instance = Post.objects.get(id=delete_reply.object_id)
            delete_reply.delete()
            data = {
                'deleted': 'Yes'
            }
            comment_slug = Post.objects.get_by_post_id(post_instance.slug)
            return redirect('blogs:detail', comment_slug.slug)
        except Exception as e:
            print(e)

    return HttpResponse(reply_id)


# Tecsee Detail Page comment and reply section
@login_required
def comment_tecsee_view(request, object_id=None):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = request.POST['parent_id']
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()
            instance = form.save(commit=False)
            instance.user = request.user  # Set the user object here
            tecsee_instance = TecseeVideo.objects.get(id=object_id)
            # if question_instance.status == 'O':
            #     question_instance.status = 'I'
            #     question_instance.save()
            instance.content_type = ContentType.objects.get_for_model(TecseeVideo)
            instance.object_id = tecsee_instance.id
            instance.parent = parent_obj
            instance.save()
            # from notifications.signals import notify
            # # if request.user != question_instance.user:
            # notify.send(request.user,
            #             recipient=question_instance.user,
            #             verb=instance.comment,
            #             target=question_instance)
            comment_slug = TecseeVideo.objects.get_by_tecsee_id(
                tecsee_instance.slug)
            commented_user = request.user.username
            tecsee_user_email = comment_slug.user.email
            tecsee_url = comment_slug.get_absolute_url()
            tecsee_title = comment_slug.title
            ticket_id = comment_slug.id
            subject = f'Teckiy New message from {commented_user} -   commented on {tecsee_title}'

            # body    = f'''Hi Teckiy,
            #                 Someone response to your question. Please check.
            #                 Thanks,
            #                 Teckiy Team
            #                 https://www.teckiy.com
            #                 !!!
            #             '''
            email = tecsee_user_email
            bcc_email = settings.ADMIN_EMAIL
            # print(email,bcc_email)
            # print('email', email)
            if settings.DEBUG:
                domain = 'http://localhost:8000'
            else:
                domain = 'https://www.teckiy.com'

            text_content = 'This is an important message.'
            html_content = render_to_string(
                'support/question_email.html', {'commented_user': commented_user,
                                                'domain': domain, 'question_url': tecsee_url, 'to_user': comment_slug.user.username})
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email],
                                         bcc=[bcc_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # if not instance.user.profile.paypal_account:
            #     messages.info(
            #         request,
            #         'Please fill your <a href="{}">paypal account</a> to redeem your points($)'.
            #         format(reverse('users:profile', kwargs={
            #                'username': instance.user.username})),
            #         extra_tags='safe'
            #     )
            # users = []
            # if instance.user != question_instance.user:
            #     users.append(instance.user)
            #     save_notification(question=question_instance,
            #                       reply_text=instance, author=question_instance.user, replied_user=instance.user,
            #                       commented_on=question_instance.slug, subject=question_instance.title)
            # # print('first instance user ', users)
            # # print('question instance user ',  question_instance.user)
            # for r in question_instance.comments.exclude(user=instance.user):
            #     # print(r.user)
            #     if r.user not in users:
            #         users.append(r.user)
            #         save_notification(comment=r, reply_text=instance.comment,
            #                           author=question_instance.user, replied_user=instance.user,
            #                           commented_on=question_instance.slug, subject=question_instance.title)
            return redirect('tecsee:detail', comment_slug.slug)

    return redirect('tecsee:all-videos')


# @login_required
# def comment_tecsee_reply_view(request, post_id=None):
#     # print(request.method)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         # print(form)
#         print('Is it working')
#         if form.is_valid():
#             parent_obj = None
#             try:
#                 parent_id = request.POST['parent_id']
#             except:
#                 parent_id = None
#             if parent_id:
#                 parent_qs = Comment.objects.filter(id=parent_id)
#                 if parent_qs.exists():
#                     parent_obj = parent_qs.first()
#             instance = form.save(commit=False)
#             instance.user = request.user  # Set the user object here
#             tecsee_instance = TecseeVideo.objects.get(id=post_id)
#             instance.content_type = ContentType.objects.get_for_model(Post)
#             instance.object_id = tecsee_instance.id
#             instance.parent = parent_obj
#             # instance.post = post_instance
#             instance.save()

#             # instance = Comment.objects.all().order_by("-id")[0]
#             # print(instance)
#             comment_slug = TecseeVideo.objects.get_by_post_id(tecsee_instance.slug)
#             # comment_slug = Post.objects.filter(id=post_id)
#             return redirect('tecseevideo:detail', comment_slug.slug)
#     return redirect('tecseevideo:all-videos')