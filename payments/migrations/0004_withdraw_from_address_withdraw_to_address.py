# Generated by Django 5.1.2 on 2024-11-07 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_deposit_from_address_deposit_to_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraw',
            name='from_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='withdraw',
            name='to_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]