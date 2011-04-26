from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    # accounts
    (r'^accounts/login/$',  'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # tutors
    (r'^tutors/create/$', 'tutordb.views.create_tutor' ),
    (r'^my/$',            'tutordb.views.my'           ),
    (r'^my/add_centre$',  'tutordb.views.add_centre'   ),
    
    # centres
    (r'^centres/', include('centres.urls') ),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Homepage:
    (r'^$', 'tutordb.views.index'),

)
