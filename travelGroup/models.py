from django.db import models
from django import forms


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=64)  # todo da modificare(?)

    def __str__(self):
        return self.name + " " + self.surname


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name="Trip Name")
    destination = models.CharField(max_length=64, verbose_name="Trip Destination")
    departure_date = models.DateField(verbose_name="Departure Date")
    arrival_date = models.DateField(verbose_name="Arrival Date")
    participants = models.ManyToManyField(User)

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


class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Sender")
    recipient = models.EmailField(max_length=254, verbose_name="Recipient")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip's Invitation")
    state = models.BooleanField(default=False, verbose_name="State")

    # TODO: to check
    def __str__(self):
        return "Invitation for " + str(self.recipient) + " to " + str(self.trip)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=300, verbose_name="Content")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip")

    # TODO: to check
    def __str__(self):
        # todo: commenti da eliminare
        # il metodo __str__ in un model serve per dare una breve descrizione del record,
        # non si dovrebbe esplicitare ogni campo
        # vedere questo link https://stackoverflow.com/questions/45483417/what-is-doing-str-function-in-django
        return "Comment id" + str(self.id)
