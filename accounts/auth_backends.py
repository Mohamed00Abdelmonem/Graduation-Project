# accounts/auth_backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

class NationalIDAuthenticationBackend(BaseBackend):
    def authenticate(self, request, national_id=None, password=None):
        try:
            # Try to find the user using the national_id (stored as a unique field)
            user = User.objects.get(profile__national_id=national_id)  # Make sure your User model has a profile with a national_id
            if user.check_password(password):  # Check if the password matches
                return user
        except ObjectDoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
