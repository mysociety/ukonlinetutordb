from django.conf.urls.defaults import *
from django.contrib            import admin

import settings

# find all the admin setup
admin.autodiscover()

# accounts
urlpatterns = patterns('django.contrib.auth.views',
    ( r'^accounts/login/$',  'login'          ),
    ( r'^accounts/logout/$', 'logout'         ),

    ( r'^accounts/reset/$',          'password_reset'          ),
    ( r'^accounts/reset_done/$',     'password_reset_done'     ),
    ( r'^accounts/reset_confirm/(?P<uidb36>\d+)/(?P<token>[\d\w-]+)$','password_reset_confirm'  ),
    ( r'^accounts/reset_complete/$', 'password_reset_complete' ),

    ( r'^accounts/password_change/$',      'password_change'      ),
    ( r'^accounts/password_change_done/$', 'password_change_done' ),

)

urlpatterns += patterns('tutordb.views.tutor',
    ( r'^$',                'index'        ),
    ( r'^my/$',             'my'           ),
    ( r'^my/add_centre$',   'add_centre'   ),    
    ( r'^my/edit_user_details$', 'edit_user_details' ),    
    ( r'^tutors/',          'tutor_list'   ),
)

# centres
urlpatterns += patterns('tutordb.views.centre',
    ( r'^centres/$',                    'centre_list'   ),
    ( r'^centres/(?P<centre_id>\d+)/$', 'centre_detail' ),
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
