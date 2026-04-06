from django.urls import path
from . views import RecordCreateView, RecordListView
urlpatterns=[
    path('',RecordCreateView.as_view(),name='records'),
    path('list/',RecordListView.as_view(),name='records_list'),
]