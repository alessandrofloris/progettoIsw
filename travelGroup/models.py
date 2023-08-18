from django.db import models


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
    name = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    departure_date = models.DateField("departure date")
    arrival_date = models.DateField("arrival date")
    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
    def check_dates(self):
        return self.arrival_date >= self.departure_date


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    start_date = models.DateTimeField("start date")
    end_date = models.DateTimeField("end date")

    def __str__(self):
        return self.name
    
    def check_dates(self):
        return self.end_date >= self.start_date


class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.EmailField(max_length=254, unique=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    # TODO: to check
    def __str__(self):
        return "Invitation id:" + str(self.id)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    # TODO: to check
    def __str__(self):
        # todo: commenti da eliminare
        # il metodo __str__ in un model serve per dare una breve descrizione del record,
        # non si dovrebbe esplicitare ogni campo
        # vedere questo link https://stackoverflow.com/questions/45483417/what-is-doing-str-function-in-django
        return "Comment id" + str(self.id)
