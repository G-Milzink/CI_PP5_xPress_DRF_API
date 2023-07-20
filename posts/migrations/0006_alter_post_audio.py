# Generated by Django 3.2.20 on 2023-07-20 10:31

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='audio',
            field=cloudinary.models.CloudinaryField(blank=True, default='../xPress/default_post_audio', max_length=255),
        ),
    ]
