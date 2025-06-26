#  Medicare Appointment Booking System
A Django-based Medicare web application that allows:
-  Doctors to register and manage appointments
-  Patients to book, reschedule, and delete appointments
-  Role-based login and dashboards
-  Time-slot-based scheduling
-  Appointment status (Pending, Approved, Rejected)

##  Live Demo & Deployment
 **Deployed on [Render](https://render.com/)**  
 **Live Demo:** [https://medicareapp-1-qs13.onrender.com](https://medicareapp-1-qs13.onrender.com)

##  Technologies Used
- **Python 3**
- **Django 4.x**
- **HTML5** (Django Templates)
- **CSS3** (Custom + Bootstrap 5)
- **JavaScript** (for dynamic dropdowns)
- **SQLite** (default development database)
  
## Features
- Doctor & Patient registration with validations
- Filter doctors dynamically by specialty
- Prevent double bookings
- Patients can:
  - Book new appointments
  - Delete pending appointments within 24 hrs
  - Reschedule rejected appointments
- Doctors can:
  - Approve or reject appointments
- Clean, full-width Bootstrap layout

###  User Roles
- **Patients**: Register, log in, book appointments, delete/reschedule pending or rejected appointments.
- **Doctors**: Register with `@doctor.com` email, view and approve/reject appointments.

###  Appointments
- Book appointments by selecting **specialty**, then dynamically loading **doctors**.
- Time slots: 8:00 AM to 5:30 PM (in 30-min intervals).
- Appointment statuses: `Pending`, `Approved`, `Rejected`.
- Patients can delete **pending** appointments within 24 hours of booking.
- Patients can **reschedule** rejected appointments.
- Doctors can **approve** or **reject** requests.

###  Dashboards
- **Patient Dashboard**:
  - See upcoming and past appointments.
  - Book new appointment (redirects to separate form).
  - Delete or reschedule if eligible.
- **Doctor Dashboard**:
  - View all appointment requests.
  - Approve or reject appointments.
  - Welcoming message shown with their username.

###  UI & UX
- Full-width, clean layouts for:
  - Patient dashboard
  - Doctor dashboard
  - Appointment form
- Custom CSS + Bootstrap for a neat, modern design.

##  Authentication
- Built-in Django authentication.
- Separate registration pages for doctors and patients.
- Doctors must use an email ending in `@doctor.com`.
- Patients must use an email ending in `@gmail.com`.

##  How to Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/vijaya-chintapalli/MedicareApp.git
cd medicare-project

2. Create and activate virtual environment

python -m venv venv
source venv/bin/activate  

3. Install dependencies

pip install -r requirements.txt

4. Run migrations

python manage.py migrate

5. Start development server

python manage.py runserver

6. Open in browser

http://127.0.0.1:8000/


