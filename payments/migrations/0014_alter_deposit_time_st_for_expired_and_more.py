# Generated by Django 5.1.2 on 2024-11-26 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_alter_deposit_time_st_for_expired_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='time_st_for_expired',
            field=models.IntegerField(default=1732655939),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='time_st_for_expired',
            field=models.IntegerField(default=1732655939),
        ),
    ]
