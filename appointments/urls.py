# from django.urls import path
# from . views import AppointmentCreateView , AppointmentListView,records
# urlpatterns = [
#     path('', AppointmentCreateView.as_view(), name='appointments'),
#     path('list/', AppointmentListView.as_view(), name='appointments_list'),
#     path('records/', records, name='records'),
# ]

from django.urls import path
from .views import AppointmentCreateView, AppointmentUpdateView, AppointmentDeleteView, patient_records

urlpatterns = [
    path('appointments/',                    AppointmentCreateView.as_view(), name='appointments'),
    path('appointments/<int:pk>/edit/',      AppointmentUpdateView.as_view(), name='appointments_edit'),
    path('appointments/<int:pk>/delete/',    AppointmentDeleteView.as_view(), name='appointments_delete'),
    path('appointments/records/',            patient_records,                 name='patient_records'),
]