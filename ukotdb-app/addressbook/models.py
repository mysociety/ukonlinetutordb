from django.contrib.gis.db import models
from django.contrib.auth.models import User


SRID = 4326      # WGS84, the coordinate system used by the geodjango calculations 


# Create your models here.
class Centre(models.Model):

    # example codes: 'LN16LC127', 'WS04LC33'
    code      = models.CharField(max_length=20, unique=True)

    name      = models.CharField(max_length=200, unique=True)
    telephone = models.CharField(max_length=20)
    email     = models.EmailField(max_length=75)

    address   = models.TextField()
    postcode  = models.CharField(max_length=10)
    location  = models.PointField(srid=SRID)


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

