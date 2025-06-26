from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from datetime import datetime, date
from .models import DoctorProfile, Appointment
from .forms import DoctorRegisterForm, PatientRegisterForm, AppointmentForm
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, time

hours = []
for h in range(8, 18):  # 8 AM to 5 PM
    am_pm_hour = datetime.strptime(f"{h}:00", "%H:%M").strftime("%I:%M %p")
    hours.append(am_pm_hour)
    am_pm_half = datetime.strptime(f"{h}:30", "%H:%M").strftime("%I:%M %p")
    hours.append(am_pm_half)


def home(request):
    return render(request, 'home.html')


def login_view(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('role_redirect')
        messages.error(request, "Invalid credentials")
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def doctor_register(request):
    form = DoctorRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            u = form.cleaned_data
            if not u['email'].endswith('@doctor.com'):
                form.add_error('email', 'Doctor email must end with @doctor.com')
            else:
                user = User.objects.create_user(
                    username=u['username'],
                    password=u['password1'],
                    email=u['email']
                )
                user.first_name = u['name']
                user.save()
                DoctorProfile.objects.create(user=user, specialty=u['specialty'])
                return redirect(f'/login/?username={u["username"]}')
        except IntegrityError:
            form.add_error('email', 'Email or username already registered.')
    else:
        if request.method == 'POST':
            print("Doctor Register Form errors:", form.errors)

    return render(request, 'registration/doctor_register.html', {'form': form})


def patient_register(request):
    form = PatientRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            u = form.cleaned_data
            if not u['email'].endswith('@gmail.com'):
                form.add_error('email', 'Patient email must end with @gmail.com')
            else:
                user = User.objects.create_user(
                    username=u['username'],
                    password=u['password1'],
                    email=u['email']
                )
                user.first_name = u['name']
                user.save()
                return redirect('login')
        except IntegrityError:
            form.add_error('email', 'Email or username already registered.')
    else:
        if request.method == 'POST':
            print("Patient Register Form errors:", form.errors)

    return render(request, 'registration/patient_register.html', {'form': form})

@login_required
def role_redirect(request):
    user = request.user
    if user.email.endswith('@doctor.com'):
        return redirect('doctor_dashboard')
    else:
        return redirect('patient_dashboard')


@login_required
def doctor_dashboard(request):
    if not request.user.email.endswith('@doctor.com'):
        return redirect('login')

    appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time')
    context = {
        'appointments': appointments
    }
    return render(request, 'medicare/doctor_dashboard.html', context)


from datetime import datetime, date

from datetime import datetime, date

@login_required
def patient_dashboard(request):
    today = date.today()
    now = datetime.now().time()
    all_appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')

    upcoming = []
    past = []

    for appt in all_appointments:
        if appt.date > today or (appt.date == today and appt.time >= now):
            upcoming.append(appt)
        else:
            past.append(appt)

    # Generate 12-hour format times
    hours = []
    for h in range(8, 18):  # 8 AM to 5 PM
        hours.append(datetime.strptime(f"{h}:00", "%H:%M").strftime("%I:%M %p"))
        hours.append(datetime.strptime(f"{h}:30", "%H:%M").strftime("%I:%M %p"))

    return render(request, 'medicare/patient_dashboard.html', {
        'upcoming': upcoming,
        'past': past,
        'today': today.isoformat(),
        'hours': hours,
        'form': AppointmentForm(user=request.user)  
    })

@login_required
def book_appointment(request):
    time_slots = format_time_slots()
    today = date.today().isoformat()
    reschedule_id = request.GET.get('reschedule')
    instance = None

    if reschedule_id:
        instance = get_object_or_404(Appointment, id=reschedule_id, patient=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = request.user
            appt.patient_name = request.user.first_name or request.user.username
            appt.approved = False
            appt.rejected = False

            if instance:
                instance.date = appt.date
                instance.time = appt.time
                instance.reason = appt.reason
                instance.specialty = appt.specialty
                instance.doctor = appt.doctor
                instance.approved = False
                instance.rejected = False
                instance.save()
            else:
                appt.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm(user=request.user, instance=instance) if instance else AppointmentForm(user=request.user)

    return render(request, 'appointment_form.html', {
        'form': form,
        'time_slots': time_slots,
        'today': today
    })

def format_hour_to_ampm(hour):
    hour = int(hour)
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12
    return f"{display_hour:02}:00 {suffix}", f"{hour:02}:00"

def format_time_slots():
    slots = []
    for hour in range(8, 18):  # 8 AM to 5 PM
        for minute in (0, 30):
            value = f"{hour:02}:{minute:02}"
            suffix = "AM" if hour < 12 else "PM"
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0:
                display_hour = 12
            display = f"{display_hour:02}:{minute:02} {suffix}"
            slots.append((value, display))
    return slots


@login_required
def get_doctors_by_specialty(request):
    specialty = request.GET.get('specialty')
    doctors = DoctorProfile.objects.filter(specialty=specialty)
    data = {
        'doctors': [
            {
                'id': doctor.user.id,
                'name': f"Dr. {doctor.user.first_name} - {doctor.specialty}"
            } for doctor in doctors
        ]
    }
    return JsonResponse(data)



@login_required
def approve_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, doctor=request.user)
    appt.approved = True
    appt.save()
    messages.success(request, "Appointment approved.")
    return redirect('doctor_dashboard')  # ✅ fixed


@login_required
def reject_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, doctor=request.user)
    appt.delete()
    messages.success(request, "Appointment rejected.")
    return redirect('doctor_dashboard')  # ✅ fixed


from datetime import timedelta

@login_required
def delete_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, patient=request.user)
    now = datetime.now()
    time_diff = now - datetime.combine(appt.date, appt.time)

    # Allow delete only if appointment is pending and within 24 hours
    if appt.approved or time_diff.total_seconds() > 86400:  # 86400 seconds = 24 hours
        messages.error(request, "You can only delete pending appointments within 24 hours.")
        return redirect('patient_dashboard')

    if request.method == 'POST':
        appt.delete()
        messages.success(request, "Appointment deleted.")
        return redirect('patient_dashboard')

    return render(request, 'confirm_delete.html', {'appointment': appt})


@login_required
def reject_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, doctor=request.user)
    appt.rejected = True
    appt.approved = False
    appt.save()
    messages.success(request, "Appointment rejected.")
    return redirect('doctor_dashboard')


@login_required
def reschedule_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id, patient=request.user)
    if not appt.rejected:
        messages.error(request, "Only rejected appointments can be rescheduled.")
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appt.doctor = form.cleaned_data['doctor']
            appt.date = form.cleaned_data['date']
            appt.time = form.cleaned_data['time']
            appt.reason = form.cleaned_data['reason']
            appt.specialty = form.cleaned_data['specialty']
            appt.approved = False
            appt.rejected = False
            appt.save()
            messages.success(request, "Appointment rescheduled.")
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm(user=request.user, initial={
            'specialty': appt.specialty,
            'doctor': appt.doctor,
            'date': appt.date,
            'time': appt.time,
            'reason': appt.reason,
        })

    return render(request, 'appointment_form.html', {
        'form': form,
        'time_slots': format_time_slots(),
        'today': date.today().isoformat()
    })
