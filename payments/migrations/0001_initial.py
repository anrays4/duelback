# Generated by Django 5.1.2 on 2024-11-01 10:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('crypto_name', models.CharField(max_length=50)),
                ('amount_game_token', models.FloatField()),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Reject'), ('3', 'Complete')], max_length=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Deposit',
                'verbose_name_plural': 'Deposits',
                'db_table': 'deposits',
            },
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('crypto_name', models.CharField(max_length=50)),
                ('amount_game_token', models.FloatField()),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Reject'), ('3', 'Complete')], max_length=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Withdraw',
                'verbose_name_plural': 'Withdraws',
                'db_table': 'withdraws',
            },
        ),
    ]