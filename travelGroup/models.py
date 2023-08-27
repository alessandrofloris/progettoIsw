from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=False, primary_key=True)
    email = models.EmailField(max_length=30, unique=True)


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="Trip Name")
    destination = models.CharField(max_length=64, verbose_name="Trip Destination")
    departure_date = models.DateField(verbose_name="Departure Date")
    arrival_date = models.DateField(verbose_name="Arrival Date")
    participants = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name
    
    def check_dates(self):
        return self.arrival_date >= self.departure_date


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip's Activity")
    name = models.CharField(max_length=64, verbose_name="Activity Name")
    description = models.CharField(max_length=256, verbose_name="Activity Description")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    
    def __str__(self):
        return self.name

    def check_dates(self):
        return self.end_date >= self.start_date

    def check_dates_is_inside_trip_date_range(self):
        return ((self.trip.departure_date <= self.start_date.date() <= self.trip.arrival_date) and
                (self.trip.arrival_date >= self.end_date.date() >= self.trip.departure_date))


class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Sender")
    recipient = models.EmailField(max_length=254, verbose_name="Recipient")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip's Invitation")
    state = models.BooleanField(default=False, verbose_name="State")

    def __str__(self):
        return "Invitation for " + str(self.recipient) + " to " + str(self.trip)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=300, verbose_name="Content")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip")

    def __str__(self):
        return "Comment id" + str(self.id)
