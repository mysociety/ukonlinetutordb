from django.contrib.gis.db import models
from django.contrib.gis.geos import point
from django.contrib.auth.models import User

SRID = 4326      # WGS84, the coordinate system used by the geodjango calculations 

# Create your models here.
class Centre(models.Model):

    name      = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email     = models.EmailField(max_length=75)
    url       = models.URLField(verify_exists=False)

    address   = models.TextField()
    postcode  = models.CharField(max_length=10)
    location  = models.PointField(srid=SRID)
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.postcode)
    


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


class helpers():
    @classmethod
    def lat_lng_to_point( cls, lat, lng):
        return point.Point(float(lng), float(lat), srid=SRID)

