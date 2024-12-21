from django.contrib.auth.backends import BaseBackend
from .models import MyUser

class QRCodeBackend(BaseBackend):
    def authenticate(self, request, username=None, verify_code=None):
        try:
            user = MyUser.objects.get(username=username, verify_code=verify_code)
            return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None
