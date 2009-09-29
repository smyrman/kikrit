from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from kikrit.auth.models import KikritUser

class KikritUserModelBackend(ModelBackend):
	"""Use our customiced KikritUser insteas of Django default User class for
	authentication.

	"""
    def authenticate(self, username=None, password=None):
        try:
            user = KikritUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except KikritUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return KikritUser.objects.get(id=user_id)
        except KikritUser.DoesNotExist:
            return None

