from django import forms
from .models import Booking
import re

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table_number', 'date', 'time', 'guests', 'phone']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.Select(attrs={'class': 'form-control'}),
            'table_number': forms.Select(attrs={'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'value': '1'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7XXXXXXXXXX',
                'pattern': r'^\+7\d{10}$',  
                'title': 'Формат: +7XXXXXXXXXX'
            })
        }
        labels = {
            'table_number': 'Выберите столик',
            'date': 'Дата бронирования',
            'time': 'Время',
            'guests': 'Количество гостей',
            'phone': 'Номер телефона'
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+7\d{10}$', phone):  
            raise forms.ValidationError('Введите телефон в формате +7XXXXXXXXXX (10 цифр после +7)')
        return phone
    
    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests < 1:
            raise forms.ValidationError('Минимальное количество гостей - 1')
        if guests > 5:
            raise forms.ValidationError('Максимальное количество гостей за столом - 5')
        return guests