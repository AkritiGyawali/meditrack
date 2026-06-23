# from django.shortcuts import render,redirect
# from . forms import appointmentform
# # Views for this app are routed via user.urls; add handlers here if you split routes later.
# def appointments(request):
#     form=appointmentform
#     if request.method == 'POST':
#         form = appointmentform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('appointment')
#     return render(request, 'appointments.html',{'form':form})
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from rest_framework import viewsets
from .models import Appointment
from .forms import AppointmentForm
from .serializers import AppointmentSerializer
from doctors.models import Doctor
from records.models import Record

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments.html'
    success_url = reverse_lazy('appointments')

    def form_valid(self, form):
        messages.success(self.request, "Appointment created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.select_related('patient_name', 'doctor_name').all()
        context['doctors'] = Doctor.objects.all()
        context['patients'] = Record.objects.all()
        context['status_choices'] = [
            ('', 'All'), ('scheduled', 'Scheduled'),
            ('confirmed', 'Confirmed'), ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ]
        return context

class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments_edit.html'
    success_url = reverse_lazy('appointments')

    def form_valid(self, form):
        messages.success(self.request, "Appointment updated successfully.")
        return super().form_valid(form)

class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'appointments_confirm_delete.html'
    success_url = reverse_lazy('appointments')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment deleted successfully.")
        return super().delete(request, *args, **kwargs)

def patient_records(request):
    from records.models import Record
    patients = Record.objects.all()
    selected_patient = request.GET.get('patient_name')
    records = None
    total = 0
    if selected_patient:
        records = Appointment.objects.filter(
            patient_name_id=selected_patient
        ).select_related('doctor_name')
        total = records.count()
    return render(request, 'appointments.html', {
        'patients': patients,
        'selected_patient': selected_patient,
        'records': records,
        'total': total,
    })

# DRF
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        qs = Appointment.objects.all()
        doctor = self.request.query_params.get('doctor')
        status = self.request.query_params.get('status')
        date   = self.request.query_params.get('date')
        if doctor: qs = qs.filter(doctor_name_id=doctor)
        if status: qs = qs.filter(status=status)
        if date:   qs = qs.filter(date=date)
        return qs