# Generated by Django 2.2.6 on 2020-11-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0021_replynotification_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='replynotification',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
