# carbon_offset_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    car_type = models.CharField(max_length=50, choices=[
        ('small_car', 'Small Car'),
        ('luxury_car', 'Luxury Car'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('hybrid_car', 'Hybrid Car'),
        ('motorcycle', 'Motorcycle'),
    ])

class Transportation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, null=True, blank=True)
    distance = models.FloatField()
    distance_type = models.CharField(max_length=5, choices=[
        ('hour', 'Hour'),
        ('km', 'Kilometer'),
    ])
    carbon_emission = models.FloatField(null=True, blank=True)
