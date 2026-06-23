# from django import forms
# from .models import record
# from doctors.models import doctor
# from dashboard.models import dashboard

# class recordform(forms.ModelForm):
#     class Meta:
#         model = record
#         fields = ['user_name','doctor_name','diagnosis','prescription','recore_date']


#     doctor = forms.ModelChoiceField(
#         queryset=doctor.objects.all(),
#         empty_label='select a name'
#     )
#     dashboard= forms.ModelChoiceField(
#         queryset=dashboard.objects.all(),
#         empty_label='select a name'
#     )


from django import forms
from .models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['patient_name', 'age', 'gender', 'contact', 'address', 'blood_group']