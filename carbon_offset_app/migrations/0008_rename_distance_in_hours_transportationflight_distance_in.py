# Generated by Django 5.0 on 2024-02-27 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_offset_app', '0007_transportationflight_distance_in_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportationflight',
            old_name='distance_in_hours',
            new_name='distance_in',
        ),
    ]
