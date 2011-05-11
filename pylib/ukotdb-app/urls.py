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
    ( r'^$',              'index'      ),
    ( r'^my/$',           'my'         ),
    ( r'^my/add_centre$', 'add_centre' ),    
    ( r'^tutors/',        'tutor_list' ),
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
    
# include other apps
urlpatterns += patterns('',
    (r'^certificates/', include('certificates.urls') ),
    (r'^admin/',        include(admin.site.urls)     ),
)

# todo list - make it easier for all to see
from django.views.generic.simple import direct_to_template

urlpatterns += patterns('',
    (r'^todo$', direct_to_template, {'template': 'todo.html'}),
)
