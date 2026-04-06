from django.db import models
from dashboard.models import dashboard
from doctors.models import doctor

# Create your models here.
class record (models.Model):
    user_name = models.ForeignKey('dashboard.dashboard',on_delete=models.CASCADE,)
    doctor_name = models.ForeignKey('doctors.doctor',on_delete=models.CASCADE,)
    diagnosis = models.TextField()
    prescription = models.TextField()
    recore_date = models.DateField()