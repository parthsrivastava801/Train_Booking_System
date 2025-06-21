from rest_framework import serializers
from .models import Train, Booking



class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'
        read_only_fields = ['seats_available']





class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'booking_timestamp']

    def validate(self, data):
        train = data['train']
        seat_number = data['seat_number']

        # Check if seat number is within valid range
        if seat_number < 1 or seat_number > train.total_seats:
            raise serializers.ValidationError(f"Seat number must be between 1 and {train.total_seats}.")

        # Check if seat is already booked
        if Booking.objects.filter(train=train, seat_number=seat_number).exists():
            raise serializers.ValidationError(f"Seat number {seat_number} is already booked for this train.")

        return data