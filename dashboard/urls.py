# from django.urls import path
# from . import views
# urlpatterns=[
#     path('',views.dashboard,name ='dashboard'),
# ]
from django.urls import path

from .views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard'),
]