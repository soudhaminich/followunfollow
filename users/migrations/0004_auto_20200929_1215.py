# Generated by Django 2.2.6 on 2020-09-29 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200929_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraction',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='comments.Comment'),
        ),
    ]
