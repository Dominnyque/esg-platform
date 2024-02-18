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

class Flight(models.Model):
    car_type = models.CharField(max_length=50, choices=[
        ('economy', 'Economy'),
        ('premium', 'Premium'),

    ])

class TransportationFlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.OneToOneField(Car, on_delete=models.CASCADE, null=True, blank=True)
    distance = models.FloatField()
    distance_type = models.CharField(max_length=5, choices=[
        ('hour', 'Hour'),
        ('km', 'Kilometer'),
    ])
    carbon_emission = models.FloatField(null=True, blank=True)

class Boat(models.Model):
    boat_type = models.CharField(max_length=50, choices=[
        ('cruise', 'Cruise'),
        ('live_aboard', 'Live aboard'),

    ])

class TransportationBoat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boat = models.OneToOneField(Car, on_delete=models.CASCADE, null=True, blank=True)
    days = models.FloatField()
    people = models.FloatField()

    carbon_emission = models.FloatField(null=True, blank=True)

class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
