from django.urls import path
from .views import DoctorCreateView,  DoctorUpdateView, DoctorDeleteView
urlpatterns=[
    path('doctors/',DoctorCreateView.as_view(),name='doctors'),
    path('doctors/<int:pk>/edit/',DoctorUpdateView.as_view(),name='doctor_edit'),
    path('doctors/<int:pk>/delete/',DoctorDeleteView.as_view(),name='doctor_delete'),
]
