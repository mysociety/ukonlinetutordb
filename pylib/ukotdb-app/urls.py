from django.conf.urls.defaults   import *
from django.contrib              import admin
from django.views.generic.simple import direct_to_template

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

urlpatterns += patterns('tutordb.views.index',
    ( r'^$',                'index'        ),
)

urlpatterns += patterns('tutordb.views.my',
    ( r'^my/$',                  'my'                ),
    ( r'^my/add_centre$',        'add_centre'        ),
    ( r'^my/welcome$',           'welcome'           ),
    ( r'^my/edit_tutor_details$', 'edit_tutor_details' ),
)

# urlpatterns += patterns('tutordb.views.tutor',
#     # ( r'^tutors/$',                   'tutor_list' ),
#     # ( r'^tutors/(?P<centre_id>\d+)$', 'tutor_list' ),
# )

urlpatterns += patterns('tutordb.views.centre',
    ( r'^centres/$',                          'centre_list'   ),
    ( r'^centres/(?P<centre_id>\d+)/$',       'centre_detail' ),
    ( r'^centres/(?P<centre_id>\d+)/tutors$', 'centre_tutors' ),
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
    (r'^admin/certificates/summarise', 'certificates.views.summarise' ),
    (r'^admin/',        include(admin.site.urls)     ),
)

# static docs that get templated
urlpatterns += patterns('',
    (r'^todo$', direct_to_template, {'template': 'todo.html'}),
    (r'^help$', direct_to_template, {'template': 'help.html'}),
)
