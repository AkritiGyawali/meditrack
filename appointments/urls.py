from django.urls import path
from . views import AppointmentCreateView , AppointmentListView,records
urlpatterns = [
    path('', AppointmentCreateView.as_view(), name='appointments'),
    path('list/', AppointmentListView.as_view(), name='appointments_list'),
    path('records/', records, name='records'),
]

