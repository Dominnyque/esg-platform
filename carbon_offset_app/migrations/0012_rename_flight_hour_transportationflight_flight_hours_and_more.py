# Generated by Django 5.0 on 2024-02-27 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_offset_app', '0011_rename_distance_transportationflight_flight_hour'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportationflight',
            old_name='flight_hour',
            new_name='flight_hours',
        ),
        migrations.RenameField(
            model_name='transportationflight',
            old_name='num_travelers',
            new_name='travelers',
        ),
    ]
