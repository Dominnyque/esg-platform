from django.db import models

# Create your models here.
class CarbonSource(models.Model):
    trip_details = models.CharField(max_length=20, default = "First Name")