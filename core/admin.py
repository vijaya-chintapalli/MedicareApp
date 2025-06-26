from django.contrib import admin
from .models import Appointment, DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__username', 'specialty')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'approved')
    list_filter = ('approved', 'doctor', 'date')
    search_fields = ('patient__username', 'doctor__username', 'reason')
    ordering = ('-date', '-time')



