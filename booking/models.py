from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, time as datetime_time
from django.core.validators import MinValueValidator, MaxValueValidator
import re

TABLE_CHOICES = [(i, f'Стол {i}') for i in range(1, 11)]

TIME_CHOICES = [
    ('12:00', '12:00'), ('12:30', '12:30'),
    ('13:00', '13:00'), ('13:30', '13:30'),
    ('14:00', '14:00'), ('14:30', '14:30'),
    ('15:00', '15:00'), ('15:30', '15:30'),
    ('16:00', '16:00'), ('16:30', '16:30'),
    ('17:00', '17:00'), ('17:30', '17:30'),
    ('18:00', '18:00'), ('18:30', '18:30'),
    ('19:00', '19:00'), ('19:30', '19:30'),
    ('20:00', '20:00'), ('20:30', '20:30'),
    ('21:00', '21:00'), ('21:30', '21:30'),
    ('22:00', '22:00'), ('22:30', '22:30'),
    ('23:00', '23:00'), ('23:30', '23:30'),
]

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    table_number = models.IntegerField(choices=TABLE_CHOICES, verbose_name='Номер столика')
    date = models.DateField(verbose_name='Дата бронирования')
    time = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name='Время')
    guests = models.IntegerField(
        verbose_name='Количество гостей',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )
    phone = models.CharField(
        max_length=20, 
        verbose_name='Телефон',
        default='+7'
    )
    confirmed = models.BooleanField(default=False, verbose_name='Подтверждено')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    
    def __str__(self):
        return f"{self.user.username} - Стол {self.table_number} ({self.guests} чел.) {self.date} {self.time}"
    
    def get_booking_datetime(self):
        try:
            naive_datetime = datetime.combine(
                self.date, 
                datetime.strptime(self.time, '%H:%M').time()
            )
            return timezone.make_aware(naive_datetime)
        except:
            return timezone.make_aware(datetime.combine(self.date, datetime_time.min))
    
    def can_cancel(self):
        try:
            booking_datetime = self.get_booking_datetime()
            now = timezone.now()
            time_diff = booking_datetime - now
            return time_diff.total_seconds() > 10 * 3600
        except:
            return True  
    
    def time_until_booking(self):
        try:
            booking_datetime = self.get_booking_datetime()
            now = timezone.now()
            time_diff = booking_datetime - now
            
            if time_diff.total_seconds() <= 0:
                return "Бронирование уже началось"
            
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            
            if hours > 0:
                return f"{hours} ч {minutes} мин"
            return f"{minutes} мин"
        except Exception as e:
            return "Ошибка расчета времени"
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
# Create your models here.
