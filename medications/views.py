# from django.shortcuts import render,redirect 
# from .forms import medicationform
# # Create your views here.
# def medication(request):
#     form = medicationform
#     if request.method == 'POST':
#         form = medicationform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('medications')
#     return render (request,'medications.html',{'form':form})
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import medicationform
from .models import Medication
from records.models import Record
from .serializers import MedicationSerializer

from rest_framework import viewsets

class MedicationCreateView(CreateView):
    model = Medication
    form_class = medicationform
    template_name = 'medications.html'
    success_url = reverse_lazy('medications')
    
    def form_valid(self, form):
        messages.success(self.request, "Medication added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medications'] = Medication.objects.select_related('patient_name').all()
        
        context['patients']=Record.objects.all()
        return context

class MedicationUpdateView(UpdateView):
    model = Medication
    form_class = medicationform
    template_name = 'medications_edit.html'
    success_url = reverse_lazy('medications')

    def form_valid(self, form):
        messages.success(self.request, "Medication updated successfully.")
        return super().form_valid(form)

class MedicationDeleteView(DeleteView):
    model = Medication
    template_name = 'medications_confirm_delete.html'
    success_url = reverse_lazy('medications')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Medication deleted successfully.")
        return super().delete(request, *args, **kwargs)

# DRF
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    
def patient_records(request):
    patients = Record.objects.all()
    selected_patient = request.GET.get('patient_name')
    selected_patient_obj = None
    records = None
    total = 0

    if selected_patient:
        selected_patient_obj = Record.objects.filter(pk=selected_patient).first()
        records = Medication.objects.filter(patient_name_id=selected_patient)
        total = records.count()

    return render(request, 'medications.html',{
        'form': medicationform(),
        'medications': Medication.objects.select_related('patient_name').all(),
        'patients': patients,
        'selected_patient': selected_patient_obj,
        'records': records,
        'total': total,
    })
    