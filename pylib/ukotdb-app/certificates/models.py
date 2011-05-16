from django.contrib.auth.models     import User
from django.contrib.gis.db          import models

from tutordb.models import Centre
from certificates.certificate_pdf import CertificatePDF

class Certificate(models.Model):
    tutor        = models.ForeignKey(User)
    tutor_name   = models.CharField(max_length=200)
    centre       = models.ForeignKey(Centre)
    template     = models.CharField(max_length=20, default='default')
    student_name = models.CharField(max_length=100)
    course_name  = models.CharField(max_length=100)
    course_blurb = models.CharField(max_length=1000, default='')
    date_awarded = models.DateField()

    
    def __unicode__(self):
        return "%s - %s" % (self.student_name, self.course_name)


    def centre_name(self):
        """Return the centre name"""
        return self.centre.name


    def as_pdf(self):
        """Render a PDF for this certificate and return it"""

        pdf = CertificatePDF( self )
        pdf.render()
        return pdf.finish()


