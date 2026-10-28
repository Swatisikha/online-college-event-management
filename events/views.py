from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test


from .models import Event, Registration
from .forms import RegistrationForm


# Home Page
def home(request):
    events = Event.objects.all()

    return render(
        request,
        'events/home.html',
        {'events': events}
    )


# Event Registration@login_required(login_url='login')
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check duplicate registration
    already_registered = Registration.objects.filter(
        student=request.user,
        event=event
    ).exists()

    if already_registered:
        messages.warning(
            request,
            'You have already registered for this event!'
        )
        return redirect('home')

    # Check registration deadline
    if (
        event.registration_deadline
        and timezone.localdate() > event.registration_deadline
    ):
        messages.error(
            request,
            'Registration deadline has passed for this event.'
        )
        return redirect('home')

    # Check maximum participant limit
    registered_count = Registration.objects.filter(
        event=event
    ).count()

    if (
        event.max_participants is not None
        and registered_count >= event.max_participants
    ):
        messages.error(
            request,
            'Sorry, this event is full!'
        )
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.student = request.user
            registration.save()

            messages.success(
                request,
                'Registration successful!'
            )
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(
        request,
        'events/register.html',
        {'form': form, 'event': event}
    )


# Student Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            return redirect('home')

    else:
        form = UserCreationForm()

    return render(
        request,
        'events/signup.html',
        {'form': form}
    )


# Student Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'events/login.html',
        {'form': form}
    )


# Student Logout
def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('home')

# My Registrations
@login_required(login_url='login')
def my_registrations(request):
    registrations = Registration.objects.filter(
        student=request.user
    )

    return render(
        request,
        'events/my_registrations.html',
        {'registrations': registrations}
    )

# Student Dashboard
@login_required(login_url='login')
def student_dashboard(request):
    registrations = Registration.objects.filter(
        student=request.user
    )

    total_registrations = registrations.count()

    return render(
        request,
        'events/dashboard.html',
        {
            'registrations': registrations,
            'total_registrations': total_registrations
        }
    )

@user_passes_test(lambda user: user.is_staff, login_url='login')
def admin_dashboard(request):
    User = get_user_model()

    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    total_students = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).count()

    # Get all events from the database
    events = Event.objects.all().order_by('date')

    return render(
        request,
        'events/admin_dashboard.html',
        {
            'total_events': total_events,
            'total_registrations': total_registrations,
            'total_students': total_students,
            'events': events,
        }
    )