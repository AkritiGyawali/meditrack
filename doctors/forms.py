from django import forms
from .models import Doctor


class Doctorform(forms.ModelForm):
    class Meta:
        model= Doctor
        fields=['doctor_name','specialization','availability']