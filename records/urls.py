# from django.urls import path
# from . views import RecordCreateView, RecordListView
# urlpatterns=[
#     path('',RecordCreateView.as_view(),name='records'),
#     path('list/',RecordListView.as_view(),name='records_list'),
# ]

from django.urls import path
from .views import RecordCreateView, RecordUpdateView, RecordDeleteView,patient_records

urlpatterns = [
    path('records/',            RecordCreateView.as_view(),  name='records'),
    path('records/<int:pk>/edit/',   RecordUpdateView.as_view(), name='records_edit'),
    path('records/<int:pk>/delete/', RecordDeleteView.as_view(), name='records_delete'),
    path('records/patient/',patient_records,name='records_of_patient'),
]