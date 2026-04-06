from django.db import models

# Create your models here.
class doctor(models.Model):
   # id = models.int primary key autoincrement() yesto garnu pardeyna because django ley automatic id as a unique value automatic increment garxa so ....
   doctor_name=models.CharField(max_length=100)
   specialization=models.TextField()
   availability=models.TextField()
   def __str__(self):
      return self.doctor_name
