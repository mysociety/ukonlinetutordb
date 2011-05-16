from os import path
import inspect

from cStringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

# location of the certificate related assets - like backgrounds etc
assets_dir = path.join(path.dirname(__file__), 'assets')

# convenient variables
a4_height = 842
a4_width  = 595

configs = {
    'default': {
        'debug': True,
        'background': {
            'image': 'ukonline_cert.jpg',
        },
        'text_sections': [
            {
                'content': ['student_name'],
                'method':      'centre_text',
                'font-family': 'Courier-Bold',
                'font-size':   40,
                'x': 70,
                'y': 580,
                'h': 50,
                'w': a4_width - 70 * 2,
            },
            {
                'content': ['course_name'],
                'method':'centre_text',
                'font-family': 'Courier-Bold',
                'font-size': 30,
                'x': 80,
                'y': 460,
                'h': 40,
                'w': a4_width - 80 * 2, 
            },
            {
                'content': ['course_blurb'],
                'method':'centre_text',
                'font-family': 'Courier-Bold',
                'font-size': 20,
                'x': 90,
                'y': 250,
                'h': 200,
                'w': a4_width - 90 * 2, 
            },            
            {
                'content': ['tutor_name', 'date_awarded'],
                'joiner': ' - ',
                'method':'centre_text',
                'font-family': 'Courier-Bold',
                'font-size': 18,
                'x': 90,
                'y': 90,
                'h': 20,
                'w': a4_width - 90 * 2, 
            },            
            {
                'content': ['centre_name'],
                'joiner': ' - ',
                'method':'centre_text',
                'font-family': 'Courier-Bold',
                'font-size': 18,
                'x': 90,
                'y': 70,
                'h': 20,
                'w': a4_width - 90 * 2, 
            },            
        ]
        
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
        self.debug  = self.config.get('debug', False)

    
    def load_config(self, name):
        """Load the named config or raise exception if not found"""
        config = configs.get(name)
        if not config:
            raise Exception("Can't find a config entry for '%s'" % name)
        return config

        
    def render(self):
        self.render_background()
        for config in self.config['text_sections']:
            self.render_using_config( config )
        

    def render_background(self):
        # add the background image
        background_image_filename = assets_dir + '/' + self.config['background']['image']
        self.canvas.drawImage(
            background_image_filename,
            0, 0,                             # x,y, anchor bottom left
            height=a4_height, width=a4_width, # fill the page
        )
        

    def render_using_config(self, config):

        # setup method and arguments
        method = getattr( self, config['method'] )
        text   = self.extract_content(config)

        # draw outline if in debug
        if self.debug or config.get('debug'):
            self.draw_debug_outline( config )

        # render
        method( text, config )


    def extract_content(self, config):
        """extract text from certificate and return it"""
        joiner = config.get( 'joiner', ' ' )
        texts = []
        
        for k in config['content']:
            attr = getattr( self.certificate, k )
            if callable( attr ): attr = attr()
            attr = str( attr )
            texts.append( attr )

        return joiner.join( texts )
    
    
    def draw_debug_outline(self, config ):
        """draw an outline around the box"""
        canvas = self.canvas

        # don't muck up the external state
        canvas.saveState()

        # discreet - but visible
        canvas.setStrokeColorRGB( 0.9, 0.7, 0.7 )
        canvas.setFillColorRGB(   0.6, 0.6, 0.6 )
        canvas.setFont( 'Helvetica', 8 )

        # draw a box to show the extent
        canvas.rect(
            config['x'], config['y'], config['w'], config['h'], 
            stroke=1, fill=0,
        )
        
        # put in some debug info
        canvas.drawRightString(
            config['x'] + config['w'],
            config['y'] + 4,
            ', '.join(config['content'])
        )
        
        # restore state
        canvas.restoreState()
    
    
    def centre_text(self, text, config):
        """docstring for centre_text"""
        self.canvas.setFont( config['font-family'], config['font-size'] )
        self.canvas.drawCentredString(
            config['x'] + config['w'] / 2,
            config['y'] + config['h'] - config['font-size'],
            text
        )


    def finish(self):
        # finish and cleanup
        self.canvas.showPage()
        self.canvas.save()
        
        # Get the value of the StringIO buffer and write it to the response.
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf




