# Generated by Django 3.1 on 2020-09-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0010_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
