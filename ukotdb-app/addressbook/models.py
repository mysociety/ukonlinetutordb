from django.contrib.auth.models     import User
from django.contrib.gis.db          import models

from centres.models import Centre

import settings

# possibly bad name but seems appropriate
class Tenure(models.Model):
    centre = models.ForeignKey(Centre)
    user   = models.ForeignKey(User)
    
    ROLE_CHOICES = (
        ('centre_pending', 'Pending Centre Confirmation'),
        ('tutor_pending',  'Pending Tutor Confirmation'),
        ('tutor',          'Tutor'),
        ('admin',          'Centre Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ( "centre", "user" )