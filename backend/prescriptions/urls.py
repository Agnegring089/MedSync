from django.urls import path
from . import views

urlpatterns = [
    path('<int:patient_id>/', views.create_prescription, name='create_prescription'),
    path('view/<int:patient_id>/', views.view_prescriptions, name='view_prescriptions'),
    path('delete/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
]
