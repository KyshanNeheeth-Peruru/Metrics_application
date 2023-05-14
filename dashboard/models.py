from django.db import models

# Create your models here.

class Temperature(models.Model):
    time = models.DateTimeField(primary_key=True)
    value = models.FloatField()

class pH(models.Model):
    time = models.DateTimeField(primary_key=True)
    value = models.FloatField()

class DistilledOxygen(models.Model):
    time = models.DateTimeField(primary_key=True)
    value = models.FloatField()

class Pressure(models.Model):
    time = models.DateTimeField(primary_key=True)
    value = models.FloatField()
