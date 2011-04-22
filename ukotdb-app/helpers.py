import urllib2
import simplejson as json

from django.contrib.gis.geos import point

import settings

def lat_lng_to_point( lat, lng):
    return point.Point(float(lng), float(lat), srid=settings.SRID)

def postcode_to_point( postcode ):
    # get postcode from Mapit
    try:
        url = settings.MAPIT_URL + 'postcode/' + urllib2.quote(postcode)
        res = urllib2.urlopen( url )
        mapit_location = json.load( res )
    except urllib2.HTTPError:
        return None

    code = mapit_location.get('code')
    if code == 404 or code == 400:
        return None

    latitude  = mapit_location['wgs84_lat']
    longitude = mapit_location['wgs84_lon']

    return lat_lng_to_point( latitude, longitude )
