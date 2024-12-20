# Generated by Django 5.1.2 on 2024-11-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SocialForWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_name', models.CharField(max_length=100)),
                ('link', models.TextField(max_length=500)),
                ('logo', models.ImageField(upload_to='social_logo/')),
            ],
        ),
    ]
