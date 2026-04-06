from django.shortcuts import render,redirect 
from .forms import medicationform
# Create your views here.
def medication(request):
    form = medicationform
    if request.method == 'POST':
        form = medicationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medications')
    return render (request,'medications.html',{'form':form})