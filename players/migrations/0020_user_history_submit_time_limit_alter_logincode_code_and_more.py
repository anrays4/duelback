# Generated by Django 5.1.2 on 2024-11-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0019_alter_logincode_code_alter_logincode_time_st'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='history_submit_time_limit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logincode',
            name='code',
            field=models.CharField(default=645115, max_length=20),
        ),
        migrations.AlterField(
            model_name='logincode',
            name='time_st',
            field=models.CharField(default=1732663607, max_length=120),
        ),
    ]