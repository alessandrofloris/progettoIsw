from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=64) # todo da modificare(?)

class Trip(models.Model):
    name = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    departure_date = models.DateTimeField("departure date")
    arrival_date =  models.DateTimeField("arrival date")

class Activity(models.Model):
    description = models.CharField(max_length=256)
    destination = models.CharField(max_length=64)
    start_date = models.DateTimeField("start date")
    end_date =  models.DateTimeField("end date")