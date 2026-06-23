"""
URL configuration for meditrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from doctors.views import DoctorViewSet
from appointments.views import AppointmentViewSet
from medications.views import MedicationViewSet
from records.views import RecordViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'records', RecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("dashboard.urls")),
    path('',include('doctors.urls')),
    path('',include('appointments.urls')),
    path('',include('medications.urls')),
    path('',include('records.urls')),
    path('api/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
