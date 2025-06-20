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
