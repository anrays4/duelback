# Generated by Django 5.1.2 on 2024-10-31 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_game', '0021_gameroom_game_room_is_end_alter_waitingroom_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waitingroom',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 19, 14, 18, 567841, tzinfo=datetime.timezone.utc)),
        ),
    ]