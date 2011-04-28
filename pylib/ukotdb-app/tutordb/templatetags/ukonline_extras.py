import re

from django                         import template
from django.template.defaultfilters import stringfilter

@stringfilter
def to_miles(value):
    """convert metres to miles"""
    metres = float( re.sub('[^\d\.]+', '', value) )

    # 1 metre = 0.000621371192 miles
    miles = metres * 0.000621371192
    
    return "%.1f miles" % miles

register = template.Library()
register.filter('to_miles', to_miles)
