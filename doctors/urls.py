from django.urls import path
from . import views
urlpatterns=[
    path('',views.DoctorCreateView.as_view(),name='doctors'),
    path('list/',views.DoctorListView.as_view(),name='doctors_list'),
]