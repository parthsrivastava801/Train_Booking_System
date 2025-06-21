from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterUserView, 
                    LoginUserView, 
                    logout_user, 
                    TrainListView, 
                    TrainDetailView, 
                    MyBookingsView, 
                    cancel_booking,
                    RegisterView,
                    LoginView,
                    TrainViewSet,
                    BookingViewSet,
                    homepage,
                    get_available_seats)

router = DefaultRouter()
router.register(r'trains', TrainViewSet, basename='train')
router.register(r'bookings', BookingViewSet, basename='booking')


urlpatterns = [

    # API endpoints (DRF) ->
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/', include(router.urls)),

    
    # Template views ->
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('', homepage, name='homepage'),
    path('logout/', logout_user, name='logout'),
    path('trains-web/', TrainListView.as_view(), name='train_list'),
    path('trains-web/<int:pk>/', TrainDetailView.as_view(), name='train_detail'),
    path('my-bookings/', MyBookingsView.as_view(), name='my_bookings'),
    path('cancel-booking/<int:pk>/', cancel_booking, name='cancel_booking'),
    path('trains-web/<int:train_id>/available-seats/', get_available_seats, name='get_available_seats'),

    
]
