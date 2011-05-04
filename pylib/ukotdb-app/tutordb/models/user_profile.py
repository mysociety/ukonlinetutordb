from django.contrib.auth.models     import User
from django.contrib.gis.db          import models

class UserProfile(models.Model):
    user  = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
        
    class Meta:
        app_label = 'tutordb'
