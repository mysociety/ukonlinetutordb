from django.contrib.auth.models   import User
from django.contrib.auth.backends import ModelBackend

class EmailModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):

        try:
            user = User.objects.get( email=username )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass  # fall through
        
        # no user found - return None
        return None

