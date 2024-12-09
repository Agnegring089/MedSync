from rest_framework.permissions import BasePermission
from django.http import HttpResponseForbidden
from functools import wraps

class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'pharmaceutical')

# Decorador para views baseadas em funções
def pharmacist_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'pharmaceutical'):
            return HttpResponseForbidden("Acesso restrito a farmacêuticos.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
