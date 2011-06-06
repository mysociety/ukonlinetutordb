from django.contrib.gis.db          import models

from tutordb.models import Centre, Tutor

import settings

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
        return "%s - %s" % (self.user.email, self.centre.name)

    class Meta:
        unique_together = ( "centre", "tutor" )
        app_label = 'tutordb'
