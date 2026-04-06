from django.db import models
from dashboard.models import dashboard
from doctors.models import doctor
# Create your models here.
class appointment(models.Model):
    patient_name = models.ForeignKey("dashboard.dashboard",on_delete=models.CASCADE,)
    doctor_name = models.ForeignKey("doctors.doctor",on_delete=models.CASCADE,)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100)

    