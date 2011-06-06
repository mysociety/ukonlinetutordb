import re

from tutordb.forms      import CreateTutorForm, EditTutorForm
from tutordb.models     import Centre, Tenure

from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
from django.contrib.auth.models         import Group
from django.core.urlresolvers           import reverse
from django.db                          import IntegrityError
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response, get_object_or_404
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template

@login_required
def my(request):
    """Homepage for a tutor"""
    
    tutor = request.user

    # get all the centres
    tenures = Tenure.objects.all().filter(tutor=tutor)
    centres = [ t.centre for t in tenures ]

    # get recent certificates
    certificates = tutor.certificate_set.order_by('-id').all()[:10]
        
    return render_to_response(
        'tutordb/my.html',
        {
            'centres':      centres,
            'certificates': certificates,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_tutor_details(request):
    """Allow tutor to edit their own details"""

    tutor = request.user
    
    # FIXME - change to using generics now as the Tutor inherits from the user

    if request.method == 'POST':

        form = EditTutorForm(request.POST, tutor=tutor);
        
        if form.is_valid():
            cleaned_data = form.cleaned_data

            tutor.first_name = cleaned_data['name']
            tutor.last_name  = ''
            tutor.phone      = cleaned_data['phone']

            tutor.save()

            return HttpResponseRedirect( reverse( my ) )

    else:
        form = EditTutorForm(tutor=tutor)

    return render_to_response(
        'tutordb/edit_tutor_details.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )

    
@login_required
def add_centre(request):
    """Allow a tutor to add a centre to themselves"""
    
    # declare in case it gets used
    error = None
    
    # If we have a post then add centre to tutor and redirect back to '/my'
    centre_id = request.POST.get('centre_id')
    if centre_id:
        try:
            centre = Centre.objects.get(id=centre_id)
            centre.tenure_set.create(tutor=request.user, role='tutor')
        except Centre.DoesNotExist:
            error = "Could not find centre in db";
        except IntegrityError:
            # centre and user already linked - do nothing
            pass
            
        if not error:
            return HttpResponseRedirect( reverse( my ) )

    # TODO - search for name as well?
    postcode = request.GET.get('postcode')    
    if postcode:
        queryset = Centre.objects.all().near_postcode(postcode)
    else:
        queryset = Centre.objects.none()
    
    return object_list(
        request,
        template_name = 'tutordb/add_centre.html',
        paginate_by   = 5,
        allow_empty   = True,
        queryset      = queryset,
        extra_context = {
            'postcode' : postcode,
            'error'    : error,
        },
    )
