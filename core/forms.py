from django import forms
from django.contrib.auth.models import User
from .models import Appointment, DoctorProfile
from django.contrib.auth.forms import UserCreationForm

# Specialty choices
SPECIALTY_CHOICES = [
    ('Cardiology', 'Cardiology'),
    ('Gynecology', 'Gynecology'),
    ('Neurology', 'Neurology'),
    ('Psychiatry', 'Psychiatry'),
    ('Dermatology', 'Dermatology'),
    ('Pediatrics', 'Pediatrics'),
    ('Dentistry', 'Dentistry'),
    ('Orthopedics', 'Orthopedics'),
    ('ENT', 'ENT'),
    ('Oncology', 'Oncology'),
    ('General', 'General'),
    ('Radiology', 'Radiology'),
    ('Urology', 'Urology'),
    ('Endocrinology', 'Endocrinology'),
    ('Gastroenterology', 'Gastroenterology'),
    ('Nephrology', 'Nephrology'),
    ('Rheumatology', 'Rheumatology'),
    ('Pulmonology', 'Pulmonology'),
    ('Ophthalmology', 'Ophthalmology'),
]

class DoctorRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    specialty = forms.ChoiceField(choices=SPECIALTY_CHOICES)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@doctor.com'):
            raise forms.ValidationError('Doctor email must end with @doctor.com')
        return email
    
class PatientRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Patient email must end with @gmail.com')
        return email


class AppointmentForm(forms.ModelForm):
    specialty = forms.ChoiceField(choices=SPECIALTY_CHOICES, required=True)
    phone = forms.CharField(max_length=10, min_length=10, required=True)
    reason = forms.CharField(widget=forms.Textarea, required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': ''}), required=True)

    class Meta:
        model = Appointment
        fields = ['phone', 'specialty', 'doctor', 'date', 'time', 'reason']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Generate 24-hour time choices every 30 minutes
        TIME_CHOICES = [(f"{h:02}:{m:02}", f"{h:02}:{m:02}") for h in range(0, 24) for m in (0, 30)]
        self.fields['time'] = forms.ChoiceField(choices=TIME_CHOICES, required=True)

        # Doctor dropdown initially empty, filled via JS
        self.fields['doctor'].queryset = User.objects.filter(
            id__in=DoctorProfile.objects.values_list('user_id', flat=True)
        )
        self.fields['doctor'].empty_label = "Select Specialty First"
        self.fields['doctor'].required = True
