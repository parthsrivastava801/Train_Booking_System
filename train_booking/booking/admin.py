from django.contrib import admin


from django.contrib import admin
from .models import Train, Booking


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'destination', 'departure_time', 'total_seats', 'seats_available')
    search_fields = ('name', 'source', 'destination')
    list_filter = ('source', 'destination', 'departure_time')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'train', 'seat_number', 'booking_timestamp')
    search_fields = ('user__username', 'train__name')
    list_filter = ('booking_timestamp', 'train')
