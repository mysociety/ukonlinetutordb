import logging

from django.contrib.auth.models     import User, UserManager, Group
from django.contrib.gis.db          import models
from django.contrib.gis.measure     import Distance
from django.db.models.signals       import post_save

from helpers import postcode_to_point

import settings

################################################################################

# based on this blog article:
#   http://scottbarnham.com/blog/2008/08/21/extending-the-django-user-model-with-inheritance/

class Tutor(User):
    phone = models.CharField(max_length=20)
        
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def is_head_office(self):
        """docstring for is_head_office"""
        ho_group = Group.objects.get(name="Head Office")

        # check that we are either in the HO group or that we are an admin for the centre
        if ho_group in self.groups.all():
            return True
        else:
            return False

    def is_manager_of(self, underling):
        """Check if the user is manager of another user"""
        underling_centres = [ i.centre for i in underling.tenure_set.all() ]
        manager_centres   = [ i.centre for i in self.tenure_set.filter(role='admin').all() ]

        for man_centre in manager_centres:
            if man_centre in underling_centres:
                return True

        return False
        
            

    def __unicode__(self):
        return self.email


# TODO - When a User is created directly (eg during the initial db sync) no
# matching tutor is created. This means that the user cannot log in until an
# entry in the 'tutors' table is created.
#
# This should ideally be done using signals - but not going to attempt that code
# until we have a stable django version to target.


#############################################################################


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
    
    def is_tutor_admin(self, tutor):
        """
        Return true if the tutor is an admin for this centre
        """
        
        if self.tenure_set.filter( tutor=tutor, role='admin' ).count():
            return True
        else:
            return False
        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.postcode)



################################################################################


# possibly bad name but seems appropriate
class Tenure(models.Model):
    centre = models.ForeignKey(Centre)
    tutor  = models.ForeignKey(Tutor)
    
    ROLE_CHOICES = (
        ('centre_pending', 'Pending Centre Confirmation'),
        ('tutor_pending',  'Pending Tutor Confirmation'),
        ('tutor',          'Tutor'),
        ('admin',          'Centre Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __unicode__(self):
        return "%s - %s" % (self.tutor.email, self.centre.name)

    class Meta:
        unique_together = ( "centre", "tutor" )

