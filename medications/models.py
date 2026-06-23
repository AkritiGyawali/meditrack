from django.db import models
from records.models import Record
# Create your models here.
class Medication(models.Model):
    # user_name = models.ForeignKey('dashboard.dashboard',on_delete=models.CASCADE,on_update=models.CASCADE,) # in django foreign key only appects on_delete. It doesn't accept on_update .
    # doctor_name = models.ForeignKey('doctors.doctor',on_delete=models.CASCADE,on_update=models.CASCADE,)
    patient_name = models.ForeignKey(Record, on_delete=models.CASCADE, null=True, blank=True)
    medication_name = models.CharField(max_length=100,default='')
    dosage = models.CharField(max_length=100,default='')
    frequency = models.CharField(max_length=100,default='')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.medication_name