# Generated by Django 5.0 on 2024-02-27 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_offset_app', '0010_remove_transportationflight_distance_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportationflight',
            old_name='distance',
            new_name='flight_hour',
        ),
    ]