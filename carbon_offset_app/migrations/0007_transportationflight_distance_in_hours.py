# Generated by Django 5.0 on 2024-02-27 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_offset_app', '0006_rename_fright_hours_transportationflight_flight_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportationflight',
            name='distance_in_hours',
            field=models.CharField(choices=[('hour', 'Hour'), ('km', 'Kilometer')], default=1, max_length=5),
            preserve_default=False,
        ),
    ]