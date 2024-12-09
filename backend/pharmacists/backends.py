# farmaceuticos/backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Pharmaceutical

class CRFAuthBackend(BaseBackend):
    """
    Autentica farmacêuticos usando o CRF e a senha.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            pharmaceutical = Pharmaceutical.objects.get(crf=username)
            user = pharmaceutical.user
            if user.check_password(password):
                if user.is_active and pharmaceutical.status:
                    return user
        except Pharmaceutical.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
