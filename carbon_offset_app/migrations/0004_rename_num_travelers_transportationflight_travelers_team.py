# Generated by Django 5.0 on 2024-02-27 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carbon_offset_app', '0003_transportationflight_num_travelers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportationflight',
            old_name='num_travelers',
            new_name='travelers_team',
        ),
    ]
