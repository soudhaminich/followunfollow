# Generated by Django 2.2.6 on 2020-12-14 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tecsee', '0002_tecseevideo_approved'),
        ('analytics', '0006_auto_20201207_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectviewed',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tecsee.TecseeVideo'),
        ),
    ]
