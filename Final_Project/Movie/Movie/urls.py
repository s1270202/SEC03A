"""
URL configuration for Movie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MovieApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('movie_selection/', views.movie_selection_view, name='movie_selection'),
    path('date_selection/', views.date_selection_view, name='date_selection'),
    path('seat_selection/', views.seat_selection_view, name='seat_selection'),
    path('register/', views.user_registration_view, name='register'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('view_reservations/', views.view_reservations, name='view_reservations'),
    path('reservation_history/', views.reservation_history_view, name='reservation_history'),
    path('view_reservation/', views.view_reservation, name='view_reservation'),
    path('logout/', views.logout, name='logout'),
]
