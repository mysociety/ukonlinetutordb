from os import path
import inspect
import copy
import logging

from cStringIO            import StringIO
                          
from reportlab.lib.colors      import Color
from reportlab.lib.enums       import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles      import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase         import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen          import canvas
from reportlab.platypus        import Paragraph, Frame
import reportlab.rl_config

# location of the certificate related assets - like backgrounds etc
assets_dir = path.join(path.dirname(__file__), 'assets')

# convenient variables
a4_height = 842
a4_width  = 595
minimum_font_size = 6

# load the extra fonts we need 


# if some glyphs are missing we can  suppress warnings
# reportlab.rl_config.warnOnMissingFontGlyphs = 0

# these fonts are installed by the 'ttf-mscorefonts-installer' debian package
pdfmetrics.registerFont(TTFont('Verdana',             '/usr/share/fonts/truetype/msttcorefonts/Verdana.ttf'))
pdfmetrics.registerFont(TTFont('Verdana_Bold',        '/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Verdana_Italic',      '/usr/share/fonts/truetype/msttcorefonts/Verdana_Italic.ttf'))
pdfmetrics.registerFont(TTFont('Verdana_Bold_Italic', '/usr/share/fonts/truetype/msttcorefonts/Verdana_Bold_Italic.ttf'))

# TODO - change the 'content' list to be a function?

configs = {
    'default': {
        # 'debug': True,
        'background': {
            'image': 'pcb_green.jpg',
        },
        'text_section_defaults': {
            'text-align':  'centre',
            'font-family': 'Courier-Bold',
            'overflow':    'shrink',
        },
        'text_sections': [
            {
                'content':   ['student_name'],
                'font-size': 40,
                'x':         70,
                'y':         585,
                'h':         50,
                'w':         a4_width - 70 * 2,
            },
            {
                'content':   ['course_name'],
                'font-size': 30,
                'x':         80,
                'y':         460,
                'h':         40,
                'w':         a4_width - 80 * 2, 
            },
            {
                'content':   ['course_blurb'],
                'font-size': 20,
                'overflow':  'wrap',
                'x':         90,
                'y':         250,
                'h':         200,
                'w':         a4_width - 90 * 2, 
            },            
            {
                'content':   ['tutor_name', 'date_awarded'],
                'joiner':    ' - ',
                'font-size': 18,
                'x':         90,
                'y':         90,
                'h':         20,
                'w':         a4_width - 90 * 2, 
            },            
            {
                'content':   ['centre_name'],
                'font-size': 18,
                'x':         90,
                'y':         70,
                'h':         20,
                'w':         a4_width - 90 * 2, 
            },            
        ]
        
    },
    'dc_pito': {
        'debug': False,
        'background': {
            'image': 'dc_pito.jpg',
        },
        'text_section_defaults': {
            'text-align':  'centre',
            'font-family': 'Verdana',
            'overflow':    'shrink',
        },
        'text_sections': [
            {
                'content':   ['student_name'],
                'font-size': 32,
                'x':         70,
                'y':         495,
                'h':         50,
                'w':         a4_width - 70 * 2,
            },
            {
                'content':   ['tutor_name'],
                'text-align': 'left',
                'font-size': 24,
                'x':         370,
                'y':         441,
                'h':         30,
                'w':         210, 
            },            
            {
                'content':   ['course_blurb'],
                'font-family': 'Verdana_Italic',
                'font-size': 24,
                'overflow':  'wrap',
                'x':         120,
                'y':         270,
                'h':         120,
                'w':         a4_width - 120 * 2, 
            },            
            {
                'content':   ['centre_name'],
                'font-size': 20,
                'x':         90,
                'y':         170,
                'h':         30,
                'w':         a4_width - 90 * 2, 
            },            
        ]
        
    },
}

# alter the default design for the different backgrounds
configs['pcb_green'] = copy.deepcopy( configs['default'] )
configs['pcb_red']   = copy.deepcopy( configs['default'] )
configs['pcb_red']['background']['image'] = 'pcb_red.jpg'


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
        self.config = self.load_config( certificate.template.slug )
        self.debug  = self.config.get('debug', False)
        
        # extract the text section configs and apply defaults
        self.text_section_configs = []
        defaults = self.config['text_section_defaults']
        
        for c in self.config['text_sections']:
            for k in defaults:
                if k not in c:
                    c[k] = defaults[k]
            self.text_section_configs.append(c)
    
    def load_config(self, name):
        """Load the named config or raise exception if not found"""
        config = configs.get(name)
        if not config:
            raise Exception("Can't find a config entry for '%s'" % name)
        return config

        
    def render(self):
        self.render_background()
        for config in self.text_section_configs:
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

        # draw outline if in debug
        if self.debug or config.get('debug'):
            self.draw_debug_outline( config )
            
        # get the text to render
        text = self.extract_content(config)

        # choose the method to draw the string
        text_align = config['text-align']

        if text_align == 'centre':
            style_alignment = TA_CENTER
        elif text_align == 'left':
            style_alignment = TA_LEFT
        else:
            raise Exception( "Unhandled value for 'text-align': '%s'" % text_align )

        if config['overflow'] == 'wrap':
            frame = Frame( config['x'], config['y'], config['w'], config['h'], )
        
            # create a paragraph style
            font_size = config['font-size']                
            style = ParagraphStyle( name='test' )
            style.fontName  = config['font-family']
            style.alignment = style_alignment
        
            while font_size > minimum_font_size:
                style.fontSize = font_size
                style.leading  = font_size
        
                para =  Paragraph( text, style )
        
                if frame.add( para, self.canvas ):
                    break
        
                # Paragraph was too big - shrink the font size
                font_size -= 1
                
        
        elif config['overflow'] == 'shrink':
            
            font_size = config['font-size']                
        
            while font_size > minimum_font_size:
                self.canvas.setFont( config['font-family'], font_size )
                if self.canvas.stringWidth(text) <= config['w']:
                    break
                font_size -= 1
            
            if text_align == 'centre':
                self.canvas.drawCentredString(
                    config['x'] + config['w'] / 2,
                    config['y'] + config['h'] - config['font-size'],
                    text
                )
            elif text_align == 'left':
                self.canvas.drawString(
                    config['x'],
                    config['y'] + config['h'] - config['font-size'],
                    text
                )
            else:
                raise Exception( "Unhandled value for 'text-align': '%s'" % text_align )
                                
        else:
            raise Exception( "Unhandled value of 'overflow': '%s'" % config['overflow'])


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
    
    
    def finish(self):
        # finish and cleanup
        self.canvas.showPage()
        self.canvas.save()
        
        # Get the value of the StringIO buffer and write it to the response.
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf




