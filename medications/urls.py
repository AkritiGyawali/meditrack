from django.urls import path
from . import views
urlpatterns=[
   path ('/api/medications',views.medication,name='medications')
]