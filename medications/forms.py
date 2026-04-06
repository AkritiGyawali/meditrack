from django import forms
from .models import medication
from doctors.models import doctor
from dashboard.models import dashboard
class medicationform(forms.ModelForm):

    class Meta:
        model = medication
        fields = ['user_name','doctor_name','dosage','start_date']

    
    doctor = forms.ModelChoiceField(
        queryset=doctor.objects.all(),
        empty_label='select a name'
    )
    dashboard = forms.ModelChoiceField(
        queryset=dashboard.objects.all(),
        empty_label='select a name'
    )