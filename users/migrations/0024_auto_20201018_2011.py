# Generated by Django 2.2.6 on 2020-10-19 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20201010_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
