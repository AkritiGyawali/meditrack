from django.shortcuts import render,redirect
from .forms import dashboardform
# Create your views here.
def dashboard(request):
    if request.method=='POST':
        form = dashboardform(request.POST) 
        if form.is_valid:
            form.save()
            return redirect('dashboard')
    return render(request,'dashboard.html')