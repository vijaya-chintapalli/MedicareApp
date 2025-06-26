from django.shortcuts import redirect
from django.urls import reverse

class PreventBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        public_paths = [
            reverse('home'),               # '/'
            reverse('login'),              # '/login/'
            reverse('patient_register'),   # '/register/patient/'
            reverse('doctor_register'),    # '/register/doctor/'
        ]

        if not request.user.is_authenticated and request.path not in public_paths:
            return redirect('login')

        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
