from os import path

from django.contrib.auth.models     import User
from django.contrib.gis.db          import models

from cStringIO import StringIO
from reportlab.pdfgen import canvas

from tutordb.models import Centre

# location of the certificate related assets - like backgrounds etc
assets_dir = path.join(path.dirname(__file__), 'assets')

# convenient variables
a4_height = 842
a4_width  = 595

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
        """Render a PDF for this certificate and return it"""

        # TODO: format date nicely
        # TODO: wrap the course_blurb
        # TODO: detect overflow and cope using font scaling or wrapping

        # create the pdf canvas to work on
        pdf_buffer = StringIO()
        pdf_canvas = canvas.Canvas( pdf_buffer, pagesize=(a4_width,a4_height) )
        
        # add the background image
        background_image_filename = assets_dir + '/ukonline_cert.jpg'
        pdf_canvas.drawImage(
            background_image_filename,
            0, 0,                             # x,y, anchor bottom left
            height=a4_height, width=a4_width, # fill the page
        )
        
        # put on the candidate details
        pdf_canvas.setFont( 'Courier-Bold', 40 )
        pdf_canvas.drawCentredString(
            a4_width/2, 600, self.student_name
        )

        # pdf_canvas.drawString(100, 650, str(self.course_blurb) )
        pdf_canvas.setFont( 'Courier-Bold', 30 )
        pdf_canvas.drawCentredString(
            a4_width/2, 470, self.course_name
        )

        pdf_canvas.setFont( 'Courier-Bold', 20 )
        pdf_canvas.drawCentredString(
            a4_width/2, 440, self.course_blurb
        )

        pdf_canvas.setFont( 'Courier-Bold', 18 )
        pdf_canvas.drawCentredString(
            a4_width/2, 90, self.tutor_name + ' - ' + str(self.date_awarded)
        )
        # pdf_canvas.drawString(100, 600, str(self.date_awarded) )
        pdf_canvas.drawCentredString(
            a4_width/2, 70, self.centre.name
        )
        # pdf_canvas.drawString(100, 550, str(self.centre.name)  )
        # pdf_canvas.drawCentredString(
        #     a4_width/2, 470, self.course_name
        # )
        
        # finish and cleanup
        pdf_canvas.showPage()
        pdf_canvas.save()
        
        # Get the value of the StringIO buffer and write it to the response.
        pdf = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf