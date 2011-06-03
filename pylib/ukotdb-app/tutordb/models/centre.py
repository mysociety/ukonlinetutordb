from django.contrib.gis.db          import models
from django.contrib.gis.measure     import Distance

from helpers import postcode_to_point

import settings

class CentreQuerySet(models.query.GeoQuerySet):
    def near_postcode( self, postcode ):
        """order by proximity to a postcode"""

        pnt = postcode_to_point(postcode)
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
    location  = models.PointField(srid=settings.SRID)

    objects   = CentreManager()

    def latitude(self):
        return self.location.y

    def longitude(self):
        return self.location.x
    
    def is_user_admin(self, user):
        """
        Return true if the user is an admin for this centre
        """
        
        if self.tenure_set.filter( user=user, role='admin' ).count():
            return True
        else:
            return False



        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.postcode)

    class Meta:
        app_label = 'tutordb'
