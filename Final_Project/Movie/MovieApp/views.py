from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Reservation, ReservationHistory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

# Create your views here.

def home_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'home.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'home.html')


def movie_selection_view(request):
    if request.method == "POST":
        selected_movie_id = request.POST['movie']
        request.session['selected_movie_id'] = selected_movie_id
        return redirect('date_selection')
    else:
        movies = Movie.objects.all()
        return render(request, 'movie_selection.html', {'movies': movies})


def date_selection_view(request):
    if request.method == "POST":

        selected_date = request.POST.get('date')
        selected_movie_id = request.session.get('selected_movie_id')


        selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()


        if selected_date_obj > datetime.now().date() + timedelta(days=14):
            return render(request, 'date_selection.html', {'error': 'Please select a date within the next 14 days.'})


        selected_movie = Movie.objects.get(id=selected_movie_id)
        show_dates = selected_movie.show_dates.all()


        if not any(show_date.date == selected_date_obj for show_date in show_dates):

            return render(request, 'date_selection.html', {'error': 'The selected date is not a showing date for this movie.'})


        request.session['selected_date'] = selected_date
        return redirect('seat_selection')

    else:
        movie_id = request.session.get('selected_movie_id')
        movie = Movie.objects.get(id=movie_id)
        context = {'movie': movie}
        return render(request, 'date_selection.html', context)


def seat_selection_view(request):
    if request.method == "POST":

        selected_seat = request.POST['seat']


        selected_movie_id = request.session.get('selected_movie_id')
        selected_date = request.session.get('selected_date')


        if Reservation.objects.filter(movie_id=selected_movie_id, date=selected_date, seat=selected_seat).exists():

            movie = Movie.objects.get(pk=selected_movie_id)
            seats = range(1, movie.cinema_hall.capacity + 1)
            return render(request, 'seat_selection.html', {'error': 'This seat is already reserved.', 'seats': seats})


        username = request.POST.get('username')
        
        request.session['selected_seat'] = int(selected_seat)
        request.session['username'] = username
        return redirect('reservation')
    else:

        selected_movie_id = request.session.get('selected_movie_id')
        if selected_movie_id is not None:
            movie = Movie.objects.get(pk=selected_movie_id)

            seats = range(1, movie.cinema_hall.capacity + 1)
        else:
            seats = []
        return render(request, 'seat_selection.html', {'seats': seats})



def user_registration_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def reservation_view(request):

    selected_movie_id = request.session.get('selected_movie_id')
    selected_date = request.session.get('selected_date')
    selected_seat = request.session.get('selected_seat')

    username = request.session.get('username')


    if selected_movie_id is None or selected_date is None or selected_seat is None:
        return redirect('movie_selection')


    existing_reservation = Reservation.objects.filter(movie_id=selected_movie_id, seat=selected_seat).exists()
    if existing_reservation:

        return render(request, 'reservation.html', {'error': 'This seat is already reserved.'})


    if request.user.is_authenticated:
        reservation = Reservation.objects.create(
            user=request.user,
            movie_id=selected_movie_id,
            seat=selected_seat,
            date=selected_date,
        )
        ReservationHistory.objects.create(
            user=request.user,
            reservation=reservation
        )

    else:
        reservation = Reservation.objects.create(
            username=username,
            movie_id=selected_movie_id,
            seat=selected_seat,
            date=selected_date,
        )


    return render(request, 'reservation.html', {'reservation': reservation})



def reservation_history_view(request):

    user = request.user

    reservations = Reservation.objects.filter(user=user)
    return render(request, 'reservation_history.html', {'reservations': reservations})

def view_reservation(request):
    if request.method == "POST":
        reservation_id = request.POST['reservation_id']
        username = request.POST['username']
        reservation = get_object_or_404(Reservation, id=reservation_id, user__username=username)
        return render(request, 'reservation.html', {'reservation': reservation})
    else:
        return redirect('home')


def logout(request):
    django_logout(request)
    return redirect('home')

@csrf_exempt
def view_reservations(request):
    if request.method == "POST":
        username = request.POST['username']
        reservation_id = request.POST['reservation_id'] 

        reservation = Reservation.objects.filter(username=username, id=reservation_id)
        return render(request, 'reservations.html', {'reservation': reservation[0]})
    else:
        return redirect('home')
