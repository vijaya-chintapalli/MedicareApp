from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Appointment

class Command(BaseCommand):
    help = 'Simulate reminders for upcoming approved appointments'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        tomorrow = now + timedelta(hours=24)

        appointments = Appointment.objects.filter(
            approved=True,
            appointment_date__range=[now.date(), tomorrow.date()]
        )

        if not appointments.exists():
            self.stdout.write("✅ No upcoming appointments in the next 24 hours.")
        else:
            for appt in appointments:
                self.stdout.write(
                    f"🔔 Reminder: {appt.patient.username}, your appointment with Dr. {appt.doctor.username} is on {appt.appointment_date} at {appt.appointment_time}"
                )
