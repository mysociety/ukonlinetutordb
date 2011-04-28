from django.conf.urls.defaults import *
from django.contrib            import admin

import settings

# find all the admin setup
admin.autodiscover()

urlpatterns = patterns('',

    # accounts
    (r'^accounts/login/$',  'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
)

urlpatterns += patterns('tutordb.views.tutor',
    # tutors
    (r'^tutors/create/$', 'create_tutor' ),
    (r'^my/$',            'my'           ),
    (r'^my/add_centre$',  'add_centre'   ),    
)

urlpatterns += patterns('tutordb.views.centre',
    # centres
    (r'^centres/$',                    'centre_list'   ),
    (r'^centres/(?P<centre_id>\d+)/$', 'centre_detail' ),
)

# server static files if needed
if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (   r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT }
        ),
    )
    

urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Homepage:
    (r'^$', 'tutordb.views.tutor.index'),
)

