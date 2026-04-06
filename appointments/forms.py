from django import forms
from .models import appointment
from doctors.models import doctor as doctor_name
from dashboard.models import dashboard as dashboard_name
from datetime import datetime
from django.utils import timezone

STATUS_CHOICES = [
    ('scheduled', 'scheduled'),
    ('completed','completed'),
    ('cancelled','cancelled'),
    ('confirmed','confirmed'),
]

class appointmentform(forms.ModelForm):
    

    doctor= forms.ModelChoiceField(
        queryset=doctor_name.objects.all(),
        empty_label='select a name'
    )    

    dashboard= forms.ModelChoiceField(
        queryset=dashboard_name.objects.all(),
        empty_label='select a name'
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    
    class Meta:
        model = appointment
        fields = ['patient_name','doctor_name','date','time','status']
        widgets={
            "date": forms.DateInput(attrs={'type':'date'}),
            "time": forms.TimeInput(attrs={'type':'time'}),
        }
    def clean(self):
        cleaned_data= super().clean()
        date= cleaned_data.get('date')
        time= cleaned_data.get('time')
        doctor = cleaned_data.get('doctor_name')
        qs = appointment.objects.none()
        
        if date and time:
            dt = datetime.combine(date, time)
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            if dt < timezone.now():
                raise forms.ValidationError("Appointment date and time cannot be in the past")
            if doctor:
                qs = appointment.objects.filter(
                    doctor_name=doctor,
                    date=date,
                    time=time,
                )
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise forms.ValidationError(
                        "This doctor already has an appointment at this time."
                    )
        return cleaned_data
    