from django.urls import path, include
from .views import RegisterUserView, LoginUserView, logout_user, TrainListView, TrainDetailView, MyBookingsView, cancel_booking



urlpatterns = [
    
    # Template views ->
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('trains-web/', TrainListView.as_view(), name='train_list'),
    path('trains-web/<int:pk>/', TrainDetailView.as_view(), name='train_detail'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path('cancel-booking/<int:pk>/', cancel_booking, name='cancel_booking'),
    
]
