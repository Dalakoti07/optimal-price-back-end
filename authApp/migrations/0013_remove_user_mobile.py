# Generated by Django 3.1 on 2020-09-21 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0012_auto_20200922_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
    ]
