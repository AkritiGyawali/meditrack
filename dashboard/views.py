# from django.shortcuts import render,redirect
# from .forms import dashboardform
# # Create your views here.
# def dashboard(request):
#     if request.method=='POST':
#         form = dashboardform(request.POST) 
#         if form.is_valid:
#             form.save()
#             return redirect('dashboard')
#     return render(request,'dashboard.html')

from django.utils import timezone
from django.shortcuts import render
from doctors.models import Doctor
from records.models import Record
from appointments.models import Appointment

def dashboard(request):
    today = timezone.now().date()
    context = {
        'total_doctors':      Doctor.objects.count(),
        'total_patients':     Record.objects.count(),
        'appointments_today': Appointment.objects.filter(date=today).count(),
        'upcoming':           Appointment.objects.filter(date__gt=today).select_related('patient_name', 'doctor_name')[:5],
    }
    return render(request, 'dashboard.html', context)