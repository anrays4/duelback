# Generated by Django 5.1.2 on 2024-11-03 11:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_game', '0033_gametable_percent_for_left_user_winner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitingroom',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 3, 11, 21, 32, 283412, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='BackgammonPlayerHistory',
        ),
    ]