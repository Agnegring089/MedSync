
from django.contrib import admin
from django.urls import path, include
from prescriptions.views import create_prescription, view_prescriptions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pharmacists.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('api/', include('patients.urls')),
    path('create_prescription/<int:patient_id>/', create_prescription, name='create_prescription'),
    path('view_prescriptions/<int:patient_id>/', view_prescriptions, name='view_prescriptions'),
]
