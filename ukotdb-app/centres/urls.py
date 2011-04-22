from django.conf.urls.defaults import *

urlpatterns = patterns('centres.views',
    (r'^$',                    'centre_list'   ),
    (r'^(?P<centre_id>\d+)/$', 'centre_detail' ),
)
