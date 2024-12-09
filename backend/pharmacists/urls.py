# farmaceuticos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_pharmaceutical, name='home_pharmaceutical'),
    path('register/', views.register_pharmaceutical, name='register_pharmaceutical'),
    path('login/', views.login_pharmaceutical, name='login_pharmaceutical'),
    path('logout/', views.logout_pharmaceutical, name='logout_pharmaceutical'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('approve_patient/<int:patient_id>/', views.approve_patient, name='approve_patient'),
    path('deny_patient/<int:patient_id>/', views.deny_patient, name='deny_patient'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('view_patient/<int:patient_id>/', views.view_patient, name='view_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]
