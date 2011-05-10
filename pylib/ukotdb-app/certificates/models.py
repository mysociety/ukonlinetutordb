from django.contrib.auth.models     import User
from django.contrib.gis.db          import models

from cStringIO import StringIO
from reportlab.pdfgen import canvas

from tutordb.models import Centre

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


    def as_pdf(self):
        """Render a PDF for this cortificate and renurn it"""

        # create the pdf canvas to work on
        pdf_buffer = StringIO()
        pdf_canvas = canvas.Canvas(pdf_buffer)
        
        # put on the candidate details
        pdf_canvas.drawString(100, 800, str(self.student_name) )
        pdf_canvas.drawString(100, 750, str(self.tutor_name)   )
        pdf_canvas.drawString(100, 700, str(self.course_name)  )
        pdf_canvas.drawString(100, 650, str(self.course_blurb) )
        pdf_canvas.drawString(100, 600, str(self.date_awarded) )
        pdf_canvas.drawString(100, 550, str(self.centre.name)  )
        
        # finish and cleanup
        pdf_canvas.showPage()
        pdf_canvas.save()
        
        # Get the value of the StringIO buffer and write it to the response.
        pdf = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf