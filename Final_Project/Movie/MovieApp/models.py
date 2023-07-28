from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from datetime import datetime

# Create your models here.

class ShowDate(models.Model):
    date = models.DateField()



class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=200)
    show_dates = models.ManyToManyField(ShowDate, related_name='movies')
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.IntegerField()
    date = models.DateField()

    


class ReservationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

