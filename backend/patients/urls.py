from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PatientRegisterView, PatientLoginView, PatientDetailsView

urlpatterns = [
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
    path('login/', PatientLoginView.as_view(), name='patient-login'),
    path('me/', PatientDetailsView.as_view(), name='patient-detail'),

    # Endpoints para JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
