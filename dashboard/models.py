from django.db import models

# Create your models here.
class Dashboard(models.Model):
    user_name = models.CharField(max_length=100)
    user_address = models.TextField()
    user_phone = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_name