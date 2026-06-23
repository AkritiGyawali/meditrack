from django.db import models
from records.models import Record
from doctors.models import Doctor
# Create your models here.

STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('confirmed','confirmed'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
]
class Appointment(models.Model):
    patient_name = models.ForeignKey(Record, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name} - {self.date} {self.time}"