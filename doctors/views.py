# from django.shortcuts import render,redirect
# from .forms import Doctorform
# # Create your views here.
# def doctor(request):
#     if request.method=='POST':
#         form = Doctorform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('doctors')
    
#     return render(request,'doctors.html')

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import Doctorform
from .models import doctor

class DoctorCreateView(CreateView):
    model = doctor
    form_class = Doctorform
    template_name = "doctors.html"
    success_url = reverse_lazy("doctors")

    def form_valid(self, form):
        messages.success(self.request, "Doctor saved successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = doctor.objects.all()
        return context

class DoctorListView(ListView):
    model = doctor
    template_name = "doctors_list.html"
    context_object_name = "doctors"