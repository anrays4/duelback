# Generated by Django 5.1.2 on 2024-11-12 11:15

import players.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0015_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=players.models.profile_images, verbose_name='avatar'),
        ),
    ]