from celery import shared_task

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from time import sleep
from django.conf import settings
import boto3
import json
from botocore.exceptions import ClientError
from botocore.client import Config
from .models import Post
from django.contrib.auth.models import User
# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     print('Hello world')
#     return None


@shared_task
def s3_upload(photo_file, key, post_id):
    print('Hi')

    try:
        # key=uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)
        mimetype = 'video/mp4'
        s3.upload_fileobj(photo_file, settings.AWS_STORAGE_BUCKET_NAME, key,
                          ExtraArgs={
                              "ContentType": mimetype
                          })
        # url = s3.generate_presigned_url('get_object',
        #                                     Params={'Bucket': AWS_UPLOAD_BUCKET,
        #                                             'Key':key},
        #                                     )
        # url = f'https://django-s3-letslearntech.s3-us-west-2.amazonaws.com/{key}'
        # upload_url = FileTest(file_test=url,user_id=request.user.id)
        # upload_url.save()
        # print(url)
        update_create_post = Post.objects.filter(
            id=post_id).update(path=key, uploaded=True)

    except Exception as e:
        print("An error to s3", e)
    print("Upload Successfully")


@shared_task
def admin_post_send(blog_name, blog_author, url):
    user_list = User.objects.all().exclude(email=None)

    users_email = []
    for obj in user_list:
        print(obj.email)

        print(users_email)
        subject = f'Teckiy {blog_author} Posted new Blog about {blog_name}'
        print(blog_name, blog_author, url)
        body = f'''Hi Teckiy, 
                        {blog_author} has been posted new {blog_name} blog  in our Teckiy.
                        As we are all Teckibie, we thought to share with you.
                        PFB the below URL,
                        {url}
                        Thanks,
                        Teckiy Team
                        https://www.teckiy.com
                        !!!                    
                    '''
        email = 'tagnev.vengat@gmail.com'
        text_content = 'This is an important message.'
        html_content = f"""
                            <html>
                            <body>
                            <p>Hi Teckiy ,<br/>
                            <br/>
                            <br/>
                            <strong>{blog_author}</strong> has been posted new <strong>{blog_name}</strong> blog  in our Teckiy.
                            <br/>
                            <br/>
                            <br/>
                            We thought to share with you.
                            <br/>
                            <br/>
                            <br/>
                            PFB the below URL,
                            <br/>
                            <a href="{url}"><strong>{blog_name}</strong></a>
                            <br/>
                            <br/>
                            <br/>
                            Thanks,
                            <br/>
                            <br/>
                            Teckiy Team
                            <br/>
                            <br/>
                            https://www.teckiy.com
                            <br/>
                            <br/>
                            </p>
                            </body>
                            </html>
                        """
        # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,[obj.email],fail_silently=False)
        msg = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, [obj.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return 'Sent Successfully'


@shared_task
def admin_post_send_to_admin(blog_name, blog_author, url):

    admin_email = settings.ADMIN_EMAIL
    subject = f'Teckiy {blog_author} Posted new Blog about {blog_name}'
    print(blog_name, blog_author, url)
    body = f'''Hi Teckiy, 
                    {blog_author} has been posted new {blog_name} blog  in our Teckiy.
                    As we are all Teckibie, we thought to share with you.
                    PFB the below URL,
                    {url}
                    Thanks,
                    Teckiy Team
                    https://www.teckiy.com
                    !!!                    
                '''
    email = 'tagnev.vengat@gmail.com'
    text_content = 'This is an important message.'
    html_content = f"""
                        <html>
                        <body>
                        <p>Hi Teckiy ,<br/>
                        <br/>
                        <br/>
                        <strong>{blog_author}</strong> has been posted new <strong>{blog_name}</strong> blog  in our Teckiy.
                        <br/>
                        <br/>
                        <br/>
                        We thought to share with you.
                        <br/>
                        <br/>
                        <br/>
                        PFB the below URL,
                        <br/>
                        <a target="_top" href="{url}"><strong>{blog_name}</strong></a>
                        <br/>
                        <br/>
                        <br/>
                        Thanks,
                        <br/>
                        <br/>
                        Teckiy Team
                        <br/>
                        <br/>
                        https://www.teckiy.com
                        <br/>
                        <br/>
                        </p>
                        </body>
                        </html>
                    """
    # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,[obj.email],fail_silently=False)
    msg = EmailMultiAlternatives(
        subject, text_content, settings.DEFAULT_FROM_EMAIL, [admin_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return 'Sent Successfully'
