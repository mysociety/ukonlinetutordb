import re

from tutordb.forms      import CreateTutorForm, EditTutorForm
from tutordb.models     import Centre, Tenure, Tutor

from django.contrib.auth                import authenticate, login
from django.contrib.auth.models         import Group
from django.contrib.auth.decorators     import login_required
from django.core.urlresolvers           import reverse
from django.db                          import IntegrityError
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response, get_object_or_404
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template

def centre_list(request):
    """Show list of centres near a postcode"""
    
    postcode = request.GET.get('postcode')    

    if postcode:
        queryset = Centre.objects.all().near_postcode(postcode)
    else:
        queryset = Centre.objects.none()
    
    return object_list(
        request,
        paginate_by = 20,
        allow_empty = True,
        queryset    = queryset,
        extra_context = { 'postcode': postcode },
    )
    

def centre_detail(request, centre_id):
    """Show details of one centre"""
    
    return object_detail(
        request,
        queryset             = Centre.objects.all(),
        object_id            = centre_id,
        template_object_name = 'centre',
    )
    

@login_required
def centre_tutors(request, centre_id ):
    """Show list of centres for user to choose from"""

    centre = get_object_or_404( Centre, pk=centre_id )

    tutor = request.user
    
    # check that we are either in the HO group or that we are an admin for the centre
    if tutor.is_head_office() or centre.is_tutor_admin( tutor ):
        centre_tutor_ids = [ i.tutor.id for i in centre.tenure_set.all() ]
        queryset = Tutor.objects.filter( id__in=centre_tutor_ids )
    else:
        queryset = Tutor.objects.none()
    
    queryset = queryset.order_by('first_name')
    
    return object_list(
        request,
        template_name = 'tutordb/centre_tutor_list.html',
        paginate_by   = 40,
        allow_empty   = True,
        queryset      = queryset,
        extra_context = { "centre": centre, },
    )

    # if ho_group in tutor.groups.all():
    #     queryset = Centre.objects.all()
    # else:
    #     tutor_admin_centres = tutor.tenure_set.filter( role='admin' ).all()
    #     admin_ids = [ i.centre.id for i in tutor_admin_centres ]
    #     queryset = Centre.objects.filter( id__in=admin_ids )
    # 
    # queryset = queryset.order_by('name')
    # 
    # return object_list(
    #     request,
    #     template_name = 'tutordb/tutor_centre_list.html',
    #     paginate_by   = 40,
    #     allow_empty   = True,
    #     queryset      = queryset,
    # )

