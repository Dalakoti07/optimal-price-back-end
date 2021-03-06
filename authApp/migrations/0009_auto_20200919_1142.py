# Generated by Django 3.1 on 2020-09-19 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0015_auto_20200913_1443'),
        ('authApp', '0008_auto_20200919_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapper.product'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total_price',
            field=models.FloatField(default=models.FloatField()),
        ),
    ]
