from django.db import models


# Create your models here.


class Information(models.Model):

    drone_name = models.CharField(max_length=50, blank=True)
    drone_number = models.CharField(max_length=50, blank=True)
    long = models.FloatField(default=0, blank=True)
    lat = models.FloatField(default=0, blank=True)
