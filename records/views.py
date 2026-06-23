from django.shortcuts import render,redirect
# from .forms import recordform
# from .models import record
# from django.contrib import messages
# from django.urls import reverse_lazy
# from django.views.generic import CreateView, ListView
# # Create your views here.
# # def record(request):
# #     form=recordform
# #     if request.method=='POST':
# #         form = recordform
# #         if form.is_valid():
# #             form.save()
# #             return redirect('records')
# #     return render(request,'records.html',{'form':form})

# class RecordCreateView(CreateView):
#     model = record
#     form_class = recordform
#     template_name = "records.html"
#     success_url = reverse_lazy('records')
    
#     def form_valid(self,form):
#         messages.success(self.request, "record saved successfully")
#         return super().form_valid(form)
    
#     def form_invalid(self,form):
#         messages.error(self.request,"please correct the error below")
#         return super().form_invalid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['records'] = record.objects.select_related('user_name', 'doctor_name').all()
#         return context
    
# class RecordListView(ListView):
#     model = record
#     template = "records_list.html"
#     context_object_name = 'records'  

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from rest_framework import viewsets
from .models import Record
from .forms import RecordForm
from .serializers import RecordSerializer

class RecordListView(ListView):
    model = Record
    template_name = 'records.html'
    context_object_name = 'records'

class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    template_name = 'records.html'
    success_url = reverse_lazy('records')

    def form_valid(self, form):
        messages.success(self.request, "Record added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = Record.objects.all()
        context['patients'] = (
            Record.objects.exclude(patient_name__isnull=True)
            .exclude(patient_name__exact="")
            .values_list('patient_name', flat=True)
            .distinct()
        )
        return context

class RecordUpdateView(UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'records_edit.html'
    success_url = reverse_lazy('records')

    def form_valid(self, form):
        messages.success(self.request, "Record updated successfully.")
        return super().form_valid(form)

class RecordDeleteView(DeleteView):
    model = Record
    template_name = 'records_confirm_delete.html'
    success_url = reverse_lazy('records')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Record deleted successfully.")
        return super().delete(request, *args, **kwargs)

# DRF
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    


def patient_records(request):
    patients = (
        Record.objects.exclude(patient_name__isnull=True)
        .exclude(patient_name__exact="")
        .values_list('patient_name', flat=True)
        .distinct()
    )
    selected_patient = request.GET.get('patient_name')
    records = None
    total = 0
    if selected_patient:
        records = Record.objects.filter(patient_name=selected_patient)
        total = records.count()
    return render(request, 'records.html', {
        'patients': patients,
        'records': records,
        'selected_patient': selected_patient,
        'total': total,
    })