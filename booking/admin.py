from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'table_number', 'guests', 'date', 'time', 'phone', 'confirmed', 'created_at']
    list_filter = ['confirmed', 'date', 'user', 'guests']
    search_fields = ['user__username', 'table_number', 'phone']
    list_editable = ['confirmed']
    readonly_fields = ['created_at', 'time_until_booking_display', 'can_cancel_display']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'table_number', 'date', 'time', 'guests', 'phone', 'confirmed')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'time_until_booking_display', 'can_cancel_display'),
            'classes': ('collapse',)
        }),
    )
    
    def time_until_booking_display(self, obj):
        return obj.time_until_booking()
    time_until_booking_display.short_description = "До начала"
    
    def can_cancel_display(self, obj):
        if obj.can_cancel():
            return "Можно отменить"
        return "Нельзя отменить"
    can_cancel_display.short_description = "Можно отменить"
    
    actions = ['confirm_bookings', 'unconfirm_bookings']
    
    def confirm_bookings(self, request, queryset):
        queryset.update(confirmed=True)
        self.message_user(request, f"{queryset.count()} бронирований подтверждено")
    confirm_bookings.short_description = "Подтвердить выбранные"
    
    def unconfirm_bookings(self, request, queryset):
        queryset.update(confirmed=False)
        self.message_user(request, f"{queryset.count()} бронирований переведено в ожидание")
    unconfirm_bookings.short_description = "Снять подтверждение"