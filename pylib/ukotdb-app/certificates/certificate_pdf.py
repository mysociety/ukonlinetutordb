from os import path

from cStringIO import StringIO
from reportlab.pdfgen import canvas

# location of the certificate related assets - like backgrounds etc
assets_dir = path.join(path.dirname(__file__), 'assets')

# convenient variables
a4_height = 842
a4_width  = 595

configs = {
    'default': {
        'background': {
            'image': 'ukonline_cert.jpg',
        },
        # 'student_name': {
        #     'font-family': 'Corier-Bold',
        # },
    },
}

class CertificatePDF:
    # TODO: format date nicely
    # TODO: wrap the course_blurb
    # TODO: detect overflow and cope using font scaling or wrapping
    
    def __init__(self, certificate):
        self.certificate = certificate

        # create the buffer and canvas to work on
        self.buffer = StringIO()
        self.canvas = canvas.Canvas( self.buffer, pagesize=(a4_width,a4_height) )
    
        # choose the config
        self.config = self.load_config( certificate.template )

    
    def load_config(self, name):
        """Load the named config or raise exception if not found"""
        config = configs.get(name)
        if not config:
            raise Exception("Can't find a config entry for '%s'" % name)
        return config

        
    def render(self):
        self.render_background()
        self.render_student_name()
        self.render_course_details()
        self.render_tutor_details()
        

    def render_background(self):
        # add the background image
        background_image_filename = assets_dir + '/' + self.config['background']['image']
        self.canvas.drawImage(
            background_image_filename,
            0, 0,                             # x,y, anchor bottom left
            height=a4_height, width=a4_width, # fill the page
        )
        

    def render_student_name(self):
        # put on the candidate details
        self.canvas.setFont( 'Courier-Bold', 40 )
        self.canvas.drawCentredString(
            a4_width/2, 600, self.certificate.student_name
        )


    def render_course_details(self):
        self.canvas.setFont( 'Courier-Bold', 30 )
        self.canvas.drawCentredString(
            a4_width/2, 470, self.certificate.course_name
        )
        
        self.canvas.setFont( 'Courier-Bold', 20 )
        self.canvas.drawCentredString(
            a4_width/2, 440, self.certificate.course_blurb
        )
        

    def render_tutor_details(self):
        self.canvas.setFont( 'Courier-Bold', 18 )
        self.canvas.drawCentredString(
            a4_width/2, 90, self.certificate.tutor_name + ' - ' + str(self.certificate.date_awarded)
        )
        self.canvas.drawCentredString(
            a4_width/2, 70, self.certificate.centre.name
        )
        

    def finish(self):
        # finish and cleanup
        self.canvas.showPage()
        self.canvas.save()
        
        # Get the value of the StringIO buffer and write it to the response.
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf

