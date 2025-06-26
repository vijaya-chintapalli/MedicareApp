from django.urls import path
from .views import (
    home, login_view, logout_view,
    doctor_register, patient_register,
    role_redirect, doctor_dashboard, patient_dashboard,
    book_appointment, get_doctors_by_specialty,
    approve_appointment, reject_appointment, delete_appointment,
    reschedule_appointment  # ✅ Include this here
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/doctor/', doctor_register, name='doctor_register'),
    path('register/patient/', patient_register, name='patient_register'),

    # Dashboards
    path('dashboard/', role_redirect, name='role_redirect'),
    path('dashboard/doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', patient_dashboard, name='patient_dashboard'),

    # Booking & doctor filtering
    path('book/', book_appointment, name='book_appointment'),
    path('get_doctors_by_specialty/', get_doctors_by_specialty, name='get_doctors_by_specialty'),

    # Approve/reject/delete/reschedule appointment
    path('approve/<int:id>/', approve_appointment, name='approve_appointment'),
    path('reject/<int:id>/', reject_appointment, name='reject_appointment'),
    path('delete/<int:id>/', delete_appointment, name='delete_appointment'),
    path('reschedule/<int:id>/', reschedule_appointment, name='reschedule_appointment'),  # ✅ fixed
]
