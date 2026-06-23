from django import forms
from .models import Dashboard

class dashboardform(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['user_name','user_address','user_phone']