# Generated by Django 3.1 on 2020-08-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zip',
            field=models.CharField(max_length=9),
        ),
    ]
