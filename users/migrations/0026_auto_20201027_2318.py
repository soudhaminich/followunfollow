# Generated by Django 2.2.6 on 2020-10-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_profile_job_preferences'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='job_preferences',
        ),
        migrations.AddField(
            model_name='profile',
            name='preferences',
            field=models.CharField(blank=True, choices=[('active', 'Actively looking job right now'), ('freelancer', 'Freelancer'), ('lerning', 'Learning')], max_length=200, null=True),
        ),
    ]
