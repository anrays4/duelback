# Generated by Django 5.1.2 on 2024-11-12 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_alter_deposit_time_st_for_expired_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='time_st_for_expired',
            field=models.IntegerField(default=1731410149),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='time_st_for_expired',
            field=models.IntegerField(default=1731410149),
        ),
    ]