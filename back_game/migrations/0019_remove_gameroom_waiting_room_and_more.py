# Generated by Django 5.1.2 on 2024-10-31 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_game', '0018_gameroom_table_alter_waitingroom_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameroom',
            name='waiting_room',
        ),
        migrations.AlterField(
            model_name='waitingroom',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 12, 19, 1, 318939, tzinfo=datetime.timezone.utc)),
        ),
    ]
