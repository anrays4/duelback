# Generated by Django 5.1.2 on 2024-11-07 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_deposit_id_alter_withdraw_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='from_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='deposit',
            name='to_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
