from os import path

from cStringIO import StringIO
from reportlab.pdfgen import canvas

# location of the certificate related assets - like backgrounds etc
assets_dir = path.join(path.dirname(__file__), 'assets')

# convenient variables
a4_height = 842
a4_width  = 595

class CertificatePDF:
    # TODO: format date nicely
    # TODO: wrap the course_blurb
    # TODO: detect overflow and cope using font scaling or wrapping
    
    def __init__(self, certificate):
        self.certificate = certificate
        
    def finish(self):
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
            a4_width/2, 600, self.certificate.student_name
        )
        
        pdf_canvas.setFont( 'Courier-Bold', 30 )
        pdf_canvas.drawCentredString(
            a4_width/2, 470, self.certificate.course_name
        )
        
        pdf_canvas.setFont( 'Courier-Bold', 20 )
        pdf_canvas.drawCentredString(
            a4_width/2, 440, self.certificate.course_blurb
        )
        
        pdf_canvas.setFont( 'Courier-Bold', 18 )
        pdf_canvas.drawCentredString(
            a4_width/2, 90, self.certificate.tutor_name + ' - ' + str(self.certificate.date_awarded)
        )
        pdf_canvas.drawCentredString(
            a4_width/2, 70, self.certificate.centre.name
        )
        
        # finish and cleanup
        pdf_canvas.showPage()
        pdf_canvas.save()
        
        # Get the value of the StringIO buffer and write it to the response.
        pdf = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf