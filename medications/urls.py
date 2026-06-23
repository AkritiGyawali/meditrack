from django.urls import path
from . views import MedicationCreateView, MedicationUpdateView, MedicationDeleteView,patient_records
urlpatterns=[
   path ('medications/',MedicationCreateView.as_view(),name='medications'),
   path('medications/<int:pk>/edit/',MedicationUpdateView.as_view(),name='medication_edit'),
   path('medications/<int:pk>/delete/',MedicationDeleteView.as_view(),name='medication_delete'),
   path('medications/records/',patient_records,name='medication_records'),
]