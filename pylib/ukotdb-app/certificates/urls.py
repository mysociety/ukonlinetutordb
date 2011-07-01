from django.conf.urls.defaults import *

urlpatterns = patterns('certificates.views',
    ( r'^$',                                  'index'          ),
    ( r'^create$',                            'create'         ),
    ( r'^select_centre$',                     'select_centre'  ),
    ( r'^(?P<certificate_id>\d+)$',           'display'        ),
    ( r'^(?P<certificate_id>\d+)/pdf$',       'display_as_pdf' ),
    ( r'^(?P<certificate_id>\d+)/email_pdf$', 'email_pdf'      ),
    ( r'^tutor/(?P<tutor_id>\d+)$',           'tutor_list'     ),
)
