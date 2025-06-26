from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('django.contrib.auth.urls')),
    path('get_doctors_by_specialty/', views.get_doctors_by_specialty, name='get_doctors_by_specialty'),  
]

