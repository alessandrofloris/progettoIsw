from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=64) # todo da modificare(?)
    def __str__(self):
        return self.name + " " + self.surname

class Trip(models.Model):
    name = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    departure_date = models.DateTimeField("departure date")
    arrival_date =  models.DateTimeField("arrival date")
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    destination = models.CharField(max_length=64)
    start_date = models.DateTimeField("start date")
    end_date =  models.DateTimeField("end date")
    def __str__(self):
        return self.name