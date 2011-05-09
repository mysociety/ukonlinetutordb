from django.contrib.auth.models     import User
from django.contrib.gis.db          import models

from tutordb.models import Centre

class Certificate(models.Model):
    tutor        = models.ForeignKey(User)
    centre       = models.ForeignKey(Centre)
    student_name = models.CharField(max_length=100)
    course_name  = models.CharField(max_length=100)
    date_awarded = models.DateField()
    
    def __unicode__(self):
        return "%s - %s" % (self.student_name, self.course_name)
