from django.urls import path
from . import views

urlpatterns = [
    path('analyze_prescription/', views.analyze_prescription, name='analyze_prescription'),
]
