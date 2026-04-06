from django.db import models
from dashboard.models import dashboard
from doctors.models import doctor
# Create your models here.
class medication(models.Model):
    # user_name = models.ForeignKey('dashboard.dashboard',on_delete=models.CASCADE,on_update=models.CASCADE,) # in django foreign key only appects on_delete. It doesn't accept on_update .
    # doctor_name = models.ForeignKey('doctors.doctor',on_delete=models.CASCADE,on_update=models.CASCADE,)
    user_name = models.ForeignKey('dashboard.dashboard',on_delete=models.CASCADE,)
    doctor_name = models.ForeignKey('doctors.doctor',on_delete=models.CASCADE,)
    dosage = models.TextField()
    start_date = models.DateField()