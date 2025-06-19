from django.shortcuts import render
from django.views.generic import  FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import  redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required


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