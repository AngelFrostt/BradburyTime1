# main/views.py
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def menu(request):
    return render(request, "menu.html")

def booking(request):
    return render(request, "booking.html")

def my_bookings(request):
    return render(request, "my_bookings.html")


# Create your views here.
