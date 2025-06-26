from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialty}"

class Appointment(models.Model):
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
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    patient_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)   
    rejected = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.patient_name} with {self.doctor.get_full_name()} on {self.date} at {self.time}"
