# Generated by Django 3.1 on 2020-09-12 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0011_auto_20200912_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='product_full_spec',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='product_images',
            field=models.JSONField(),
        ),
    ]