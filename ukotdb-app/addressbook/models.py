import urllib2
import simplejson as json

from django.contrib.auth.models     import User
from django.contrib.gis.db          import models
from django.contrib.gis.geos        import point
from django.contrib.gis.measure     import Distance

import settings

SRID = 4326      # WGS84, the coordinate system used by the geodjango calculations 


class CentreQuerySet(models.query.GeoQuerySet):
    def near_postcode( self, postcode ):
        """order by proximity to a postcode"""

        pnt = helpers.postcode_to_point(postcode)
        if not pnt: return self.none()

        return self \
            .distance(pnt) \
            .order_by('distance')

class CentreManager(models.GeoManager):
    def get_query_set(self):
        return CentreQuerySet(self.model)

class Centre(models.Model):
    name      = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email     = models.EmailField(max_length=75)
    url       = models.URLField(verify_exists=False)
    address   = models.TextField()
    postcode  = models.CharField(max_length=10)
    location  = models.PointField(srid=SRID)

    objects   = CentreManager()    


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

    @classmethod
    def postcode_to_point( cls, postcode ):
        # get postcode from Mapit
        try:
            url = settings.MAPIT_URL + 'postcode/' + urllib2.quote(postcode)
            res = urllib2.urlopen( url )
            mapit_location = json.load( res )
        except urllib2.HTTPError:
            return None

        code = mapit_location.get('code')
        if code == 404 or code == 400:
            return None

        latitude  = mapit_location['wgs84_lat']
        longitude = mapit_location['wgs84_lon']

        return cls.lat_lng_to_point( latitude, longitude )
    