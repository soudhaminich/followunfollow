from celery import shared_task

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from time import sleep
from django.conf import settings
import boto3
import json
from botocore.exceptions import ClientError
from botocore.client import Config
from django.contrib.auth.models import User
# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     print('Hello world')
#     return None


@shared_task
def comment_send(commented_user,question_user_email,question_url,question_title,ticket_id):
        subject = f'Teckiy New message from {commented_user} -   {question_title} #Ticket{ticket_id}'

        # body    = f'''Hi Teckiy, 
        #                 Someone response to your question. Please check.
        #                 Thanks,
        #                 Teckiy Team
        #                 https://www.teckiy.com
        #                 !!!                    
        #             '''
        email = question_user_email
        # print('email', email)
        current_site = Site.objects.get_current()
        print(current_site.domain)

        text_content = 'This is an important message.'
        html_content = f"""
                            <html>
                            <body>
                            <p>Hi Teckiy ,<br/>
                            <br/>
                            <br/>
                            <p>Hi Teckiy, <br/>
                                <strong>{commented_user}</strong>
                                <br/>
                                    has responded to your question. CHeck here,
                                    <br/>
                                    <a href="">click here</a>
                                    <br/>
                                Thanks,<br/>
                                Teckiy Team<br/>
                                https://www.teckiy.com
                                !!!  .
                            <br/>
                            <br/>
                            <br/>
                            We thought to share with you.
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
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return 'Comment Sent'