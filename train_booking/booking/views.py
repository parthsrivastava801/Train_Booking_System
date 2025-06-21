from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import  FormView, TemplateView, ListView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import  redirect
from .forms import RegisterForm, LoginForm, BookingForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Train, Booking
from django.views import View

from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import TrainSerializer, BookingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser





# DRF API views ->
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=201)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)
    
class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['source', 'destination', 'departure_time']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.user != request.user:
            return Response({'error': 'You can only cancel your own bookings.'}, status=403)
        return super().destroy(request, *args, **kwargs)




# template based views ->
class RegisterUserView(FormView):
    template_name = 'booking/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return redirect('train_list')


class LoginUserView(FormView):
    template_name = 'booking/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome, {user.username}!")
            return redirect('train_list')
        form.add_error(None, "Invalid username or password")
        return self.form_invalid(form)


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@method_decorator(login_required, name='dispatch')
class TrainListView(ListView):
    model = Train
    template_name = 'booking/train_list.html'
    context_object_name = 'trains'

    def get_queryset(self):
        qs = Train.objects.all()
        source = self.request.GET.get('source')
        dest = self.request.GET.get('destination')
        date = self.request.GET.get('departure_time')

        if source:
            qs = qs.filter(source__icontains=source)
        if dest:
            qs = qs.filter(destination__icontains=dest)
        if date:
            qs = qs.filter(departure_time__date=date)
        return qs


@method_decorator(login_required, name='dispatch')
class TrainDetailView(View):
    def get(self, request, pk):
        train = get_object_or_404(Train, pk=pk)
        booked_seats = Booking.objects.filter(train=train).values_list('seat_number', flat=True)
        all_seats = list(range(1, train.total_seats + 1))
        available_seats = [seat for seat in all_seats if seat not in booked_seats]
        form = BookingForm(available_seats=available_seats)
        return render(request, 'booking/train_detail.html', {
            'train': train,
            'form': form,
            'available_seats': available_seats,
            'booked_seats': booked_seats
        })

    def post(self, request, pk):
        train = get_object_or_404(Train, pk=pk)
        booked_seats = Booking.objects.filter(train=train).values_list('seat_number', flat=True)
        all_seats = list(range(1, train.total_seats + 1))
        available_seats = [seat for seat in all_seats if seat not in booked_seats]
        form = BookingForm(request.POST, available_seats=available_seats)

        if form.is_valid():
            seat = int(form.cleaned_data['seat_number'])

            if seat not in available_seats:
                form.add_error('seat_number', 'Seat already booked.')
            else:
                Booking.objects.create(user=request.user, train=train, seat_number=seat)
                messages.success(request, f"Successfully booked seat {seat} on {train.name}")
                return redirect('my_bookings')

        return render(request, 'booking/train_detail.html', {
            'train': train,
            'form': form,
            'available_seats': available_seats,
            'booked_seats': booked_seats
        })


@method_decorator(login_required, name='dispatch')
class MyBookingsView(TemplateView):
    template_name = 'booking/my_bookings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = Booking.objects.filter(user=self.request.user)
        return context


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    train = booking.train
    booking.delete()
    messages.success(request, f"Canceled booking for seat {booking.seat_number} on {train.name}.")
    return redirect('my_bookings')

def homepage(request):
    if request.user.is_authenticated:
        return redirect('train_list')
    return redirect('login')

