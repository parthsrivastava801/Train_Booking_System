from django import forms
from django.contrib.auth.models import User
from .models import Booking

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        
        fields = ['username', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class BookingForm(forms.Form):
    seat_number = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        available_seats = kwargs.pop('available_seats', [])
        super().__init__(*args, **kwargs)
        self.fields['seat_number'].choices = [(seat, f"Seat {seat}") for seat in available_seats]

