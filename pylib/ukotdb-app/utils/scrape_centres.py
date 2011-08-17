# Scrape centres from the API and insert them into the database. If the centre
# already exists then update it.

import simplejson
import urllib
import sys
import os
import types
import string

sys.path.append(sys.path[0] + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings
from tutordb.models import Centre
from helpers import lat_lng_to_point

# note that the API is tricky - it wants 'method' to be the first param
base_url = 'http://www.ukonlinecentres.com/services/rest/?method=searchCentres'
base_query = {
    "api_key":    settings.UKONLINE_SERVICES_API_KEY,
    "postcode":   "SW1A1AA", # no spaces - API can't handle '+' in params
    "format":     "json",
    "numResults": 20, # appears to be ignored - but we use it below
}

# fetch 1000 results
for start in range( 1, 4000, base_query['numResults'] ):
    base_query['start'] = start
    url = base_url + '&' + urllib.urlencode( base_query )
    print "Looking at entries %s to %s: %s" % (start, start + base_query['numResults'], url)
    
    response = urllib.urlopen( url )
    json     = response.read()
    entries  = simplejson.loads( json )
    
    if type(entries) is types.DictType and entries.get('errorCode'):
        break
    
    for e in entries:                
        print "Adding/updating %s (%s)" % (e['name'], e['id'])

        # Find or create
        try:
            obj = Centre.objects.get(id=e['id'])
        except Centre.DoesNotExist:
            obj = Centre(id=e['id'])
        
        obj.name      = e['name']
        obj.telephone = e['telephone'][:20] # hack - should validate instead
        obj.email     = e['email']
        obj.url       = e['url']
        obj.address   = ', '.join([ e['address1'], e['address2'], e['address3'], e['address4'],  ])
        obj.postcode  = e['postcode']
        obj.location  = lat_lng_to_point( e['latitude'], e['longitude'] )

        # tidy up the address a little
        obj.address   = obj.address.replace(', , ', ', ')
        obj.address   = string.capwords(obj.address)
    
        obj.save()    
    
