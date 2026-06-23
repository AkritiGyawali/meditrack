from django import forms
from .models import Medication
from records.models import Record as RecordModel



class medicationform(forms.ModelForm):
    patient_name = forms.ModelChoiceField(
        queryset=RecordModel.objects.all(),
        empty_label = 'select a name',
        label = 'Patient Name'
    )
    class Meta:
        model = Medication
        fields = ['patient_name','medication_name','dosage','frequency','start_date','end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and start > end :
            raise forms.ValidationError('End date cannot be before start date.')
        return cleaned_data
    
    # doctor = forms.ModelChoiceField(
    #     queryset=doctor.objects.all(),
    #     empty_label='select a name'
    # )
    # dashboard = forms.ModelChoiceField(
    #     queryset=dashboard.objects.all(),
    #     empty_label='select a name'
    # )