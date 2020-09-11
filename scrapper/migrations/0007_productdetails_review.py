# Generated by Django 3.1 on 2020-09-11 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0006_deals'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_name', models.CharField(default='', max_length=20)),
                ('reviewer_address', models.CharField(default='', max_length=20)),
                ('review_title', models.CharField(default='', max_length=20)),
                ('ratings', models.IntegerField()),
                ('content', models.CharField(default='', max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapper.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_the_box', models.CharField(blank=True, default='', max_length=200)),
                ('model_number', models.CharField(blank=True, default='', max_length=20)),
                ('model_name', models.CharField(blank=True, default='', max_length=20)),
                ('color', models.CharField(blank=True, default='', max_length=20)),
                ('browser_type', models.CharField(blank=True, default='', max_length=20)),
                ('sim_type', models.CharField(blank=True, default='', max_length=20)),
                ('hybrid_sim_slot', models.BooleanField(blank=True, default=False)),
                ('touch_screen', models.BooleanField(blank=True, default=False)),
                ('OTG_compatible', models.BooleanField(blank=True, default=False)),
                ('sound_enhancement', models.BooleanField(blank=True, default=False)),
                ('sar_value', models.CharField(blank=True, default='', max_length=50)),
                ('display_size', models.CharField(blank=True, default='', max_length=50)),
                ('resolution', models.CharField(blank=True, default='', max_length=50)),
                ('resolution_type', models.CharField(blank=True, default='', max_length=10)),
                ('other_display_feature', models.CharField(blank=True, default='', max_length=10)),
                ('operating_system', models.CharField(blank=True, default='', max_length=20)),
                ('processor_type', models.CharField(blank=True, default='', max_length=50)),
                ('processor_core', models.CharField(blank=True, default='', max_length=20)),
                ('primary_clock_speed', models.CharField(blank=True, default='', max_length=10)),
                ('secondary_clock_speed', models.CharField(blank=True, default='', max_length=10)),
                ('operating_frequency', models.CharField(blank=True, default='', max_length=100)),
                ('internal_storage', models.CharField(blank=True, default='', max_length=10)),
                ('ram', models.CharField(blank=True, default='', max_length=10)),
                ('supported_memory_card_type', models.CharField(blank=True, default='', max_length=20)),
                ('memory_card_slot_type', models.CharField(blank=True, default='', max_length=20)),
                ('primary_camera_available', models.BooleanField(blank=True, default=False)),
                ('primary_camera', models.CharField(blank=True, default='', max_length=50)),
                ('primary_camera_features', models.CharField(blank=True, default='', max_length=1000)),
                ('secondary_camera_available', models.BooleanField(blank=True, default=False)),
                ('secondary_camera', models.CharField(blank=True, default='', max_length=50)),
                ('secondary_camera_features', models.CharField(blank=True, default='', max_length=1000)),
                ('flash', models.CharField(blank=True, default='', max_length=20)),
                ('flash_rate', models.CharField(blank=True, default='', max_length=100)),
                ('dual_camera_lens', models.CharField(blank=True, default='', max_length=20)),
                ('networking_type', models.CharField(blank=True, default='', max_length=50)),
                ('supported_network', models.CharField(blank=True, default='', max_length=100)),
                ('internet_connectivity', models.CharField(blank=True, default='', max_length=50)),
                ('three_g_speed', models.CharField(blank=True, default='', max_length=20)),
                ('gprs', models.BooleanField(blank=True, default=False)),
                ('preinstalled_browser', models.CharField(blank=True, default='', max_length=1000)),
                ('micro_usb_port', models.BooleanField(blank=True, default=False)),
                ('bluetooth_support', models.BooleanField(blank=True, default=False)),
                ('bluetooth_version', models.CharField(blank=True, default='', max_length=10)),
                ('wifi', models.BooleanField(blank=True, default=False)),
                ('wifi_version', models.CharField(blank=True, default='', max_length=20)),
                ('usb_connectivity', models.BooleanField(blank=True, default=False)),
                ('edge', models.BooleanField(blank=True, default=False)),
                ('audio_jack', models.CharField(blank=True, default='', max_length=10)),
                ('width', models.CharField(blank=True, default='', max_length=10)),
                ('height', models.CharField(blank=True, default='', max_length=10)),
                ('depth', models.CharField(blank=True, default='', max_length=10)),
                ('weight', models.CharField(blank=True, default='', max_length=10)),
                ('warranty_summary', models.CharField(blank=True, default='', max_length=100)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scrapper.product')),
            ],
        ),
    ]