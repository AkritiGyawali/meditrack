# from django.db import models
# from dashboard.models import dashboard
# from doctors.models import doctor

# # Create your models here.
# class Record (models.Model):
#     user_name = models.ForeignKey('dashboard.dashboard',on_delete=models.CASCADE,)
#     doctor_name = models.ForeignKey('doctors.doctor',on_delete=models.CASCADE,)
#     diagnosis = models.TextField()
#     prescription = models.TextField()
#     recore_date = models.DateField()

from django.db import models

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]

class Record(models.Model):
    patient_name = models.CharField(max_length=100,null=True, blank=True)
    age          = models.PositiveIntegerField(null=True, blank=True)
    gender       = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    contact      = models.CharField(max_length=15, null=True, blank=True)
    address      = models.TextField()
    blood_group  = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES,null=True, blank=True)

    def __str__(self):
        return self.patient_name or "Unknown patient"