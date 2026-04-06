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
from django.views.generic import CreateView, ListView
from django.shortcuts import render

from .forms import appointmentform
from .models import appointment
from doctors.models import doctor

class AppointmentCreateView(CreateView):
    model = appointment
    form_class = appointmentform
    template_name = "appointments.html"
    success_url = reverse_lazy("appointments")

    def form_valid(self, form):
        messages.success(self.request, "Appointment created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # show existing appointments on the same page
        context["appointments"] = appointment.objects.select_related(
            "patient_name", "doctor_name"
        ).all()
        
        return context
    
class AppointmentListView(ListView):
    model = appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        qs = (
            super().get_queryset().select_related('patient_name','doctor_name').all()
        )
        doctor_id = self.request.GET.get('doctor')
        status = self.request.GET.get('status')
        date= self.request.GET.get('date')
        
        if doctor_id:
            qs = qs.filter(doctor_name_id = doctor_id)
        if status:
            qs = qs.filter(status = status)
        if date:
            qs = qs.filter(date = date)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = doctor.objects.all()
        context['status_choices']=[
            ('','All'),
            ('scheduled','scheduled'),
            ('confirmed','confirmed'),
            ('completed','completed'),
            ('cancelled','cancelled'),
        ]
        return context
    
    

def records(request):
    
    patients = appointment.objects.values('patient_name').distinct()  # unique patient names
    selected_patient = request.GET.get('patient_name')  # from dropdown selection
    records = None
    total = 0

    if selected_patient:
        records = appointment.objects.filter(patient_name=selected_patient)
        total = records.count()

    return render(request, 'appointments.html', {
        'patients': patients,
        'selected_patient': selected_patient,
        'records': records,
        'total': total,
    })