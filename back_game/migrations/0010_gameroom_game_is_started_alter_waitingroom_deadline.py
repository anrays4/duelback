# Generated by Django 5.1.2 on 2024-10-22 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_game', '0009_gameroom_turn_tas_player_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameroom',
            name='game_is_started',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='waitingroom',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 22, 18, 10, 8, 813402, tzinfo=datetime.timezone.utc)),
        ),
    ]
