from django.db import models


# Create your models here.


class Information(models.Model):
    drone_name = models.CharField(max_length=50, blank=True)
    drone_number = models.CharField(max_length=50, blank=True)
    long = models.FloatField(default=0, blank=True)
    lat = models.FloatField(default=0, blank=True)


class Drone(models.Model):
    dev_id = models.CharField(max_length=500, blank=True)
    hardware_serial = models.CharField(max_length=500, blank=True)
    meta_data = models.DateTimeField(blank=True)


class Measures(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    key = models.CharField(max_length=50, blank=True)  # PH
    value = models.CharField(max_length=50, blank=True)  # 7

