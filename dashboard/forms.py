from django import forms
from .models import dashboard

class dashboardform(forms.ModelForm):
    class Meta:
        model = dashboard
        fields = ['user_name','user_address','user_phone']