from django.shortcuts import render,redirect
from .forms import recordform
from .models import record
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
# Create your views here.
# def record(request):
#     form=recordform
#     if request.method=='POST':
#         form = recordform
#         if form.is_valid():
#             form.save()
#             return redirect('records')
#     return render(request,'records.html',{'form':form})

class RecordCreateView(CreateView):
    model = record
    form_class = recordform
    template_name = "records.html"
    success_url = reverse_lazy('records')
    
    def form_valid(self,form):
        messages.success(self.request, "record saved successfully")
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,"please correct the error below")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = record.objects.select_related('user_name', 'doctor_name').all()
        return context
    
class RecordListView(ListView):
    model = record
    template = "records_list.html"
    context_object_name = 'records'  