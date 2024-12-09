from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_id>/', views.create_prescription, name='create_prescription'),
    path('view/<int:patient_id>/', views.view_prescriptions, name='view_prescriptions'),
]
