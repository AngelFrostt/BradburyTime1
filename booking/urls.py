from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
  path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'), 
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]