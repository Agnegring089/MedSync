from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_and_create_medicaments, name='medicament_list'),
    path('edit/<int:medicament_id>/', views.edit_medicament, name='edit_medicament'),
    path('delete/<int:medicament_id>/', views.delete_medicament, name='delete_medicament'),
]
