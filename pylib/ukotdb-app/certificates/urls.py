from django.conf.urls.defaults import *

urlpatterns = patterns('certificates.views',
    ( r'^$',                            'index'          ),
    ( r'^create$',                      'create'         ),
    ( r'^(?P<certificate_id>\d+)/$',    'display'        ),
    # ( r'^(?P<certificate_id>\d+)/pdf$', 'display_as_pdf' ),
)
