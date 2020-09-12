# Generated by Django 3.1 on 2020-09-12 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0010_auto_20200912_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='product',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='scrapper.product'),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='product_full_spec',
            field=models.JSONField(editable=False),
        ),
        migrations.AlterField(
            model_name='productdetail',
            name='product_images',
            field=models.JSONField(editable=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scrapper.product'),
        ),
    ]
