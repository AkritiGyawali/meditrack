from django import forms
from .models import doctor


class Doctorform(forms.ModelForm):
    class Meta:
        model= doctor
        fields=['doctor_name','specialization','availability']