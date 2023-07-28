from django.contrib import admin
from MovieApp.models import Movie, Reservation, ReservationHistory, CinemaHall, ShowDate

# Register your models here.

admin.site.register(Movie)
admin.site.register(Reservation)
admin.site.register(ReservationHistory)
admin.site.register(CinemaHall)
admin.site.register(ShowDate)