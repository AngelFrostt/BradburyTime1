from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Booking
from .forms import BookingForm

@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            if booking.guests > 5:
                messages.error(request, 'Максимальное количество гостей за столом - 5')
                return render(request, 'booking/create_booking.html', {'form': form})
            
            booking.save()
            messages.success(request, f'Бронирование создано! На {booking.guests} гостей. Ожидайте подтверждения.')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'booking/create_booking.html', {'form': form})

@login_required 
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'booking/my_booking.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.can_cancel():
        booking.delete()
        messages.success(request, "Бронирование успешно отменено!")
    else:
        messages.error(
            request, 
            f"Нельзя отменить бронирование менее чем за 10 часов до начала. "
            f"До вашего бронирования осталось: {booking.time_until_booking()}"
        )
    
    return redirect('my_bookings')