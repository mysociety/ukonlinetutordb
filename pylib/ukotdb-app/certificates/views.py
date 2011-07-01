from django.contrib.auth.decorators     import login_required
from django.core.urlresolvers           import reverse
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response, get_object_or_404, redirect
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template
from django.http                        import Http404


from tutordb.models      import Tutor, Centre
from certificates.models import Certificate
from certificates.forms  import CertificateForm


def check_user_may_see( request, certificate_tutor ):
    """Check that the current user may see the requested details"""
    req_tutor = request.user
    if req_tutor == certificate_tutor or req_tutor.is_head_office() or req_tutor.is_manager_of(certificate_tutor):
        pass
    else:
        raise Http404



@login_required
def index(request):
    """show the certificates nav page"""    

    return object_list(
        request,
        template_name = 'certificates/index.html',
        paginate_by   = 40,
        allow_empty   = True,
        queryset      = request.user.certificate_set.order_by('-id'),
        extra_context = {},
    )
    

# TODO - factor out common access control tests from the display, display_as_pdf
# and tutor_list functions

@login_required
def display(request, certificate_id):
    """Display a certificate"""
    
    # load the certificate
    certificate = get_object_or_404( Certificate, pk=certificate_id )
    certificate_tutor = certificate.tutor

    check_user_may_see( request, certificate_tutor )
    
    return object_detail(
        request,
        queryset  = certificate_tutor.certificate_set,
        object_id = certificate_id,
    )
    

@login_required
def display_as_pdf(request, certificate_id):
    """Create a PDF for certificate"""

    # load the certificate
    certificate = get_object_or_404( Certificate, pk=certificate_id )
    certificate_tutor = certificate.tutor

    check_user_may_see( request, certificate_tutor )
    
    # create the pdf
    pdf = certificate.as_pdf()

    # set up the response for pdf
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=certificate_%s.pdf' % certificate_id
    response.write(pdf)
    return response


@login_required
def select_centre(request):
    """Select a centre to use for the certificate"""
    tutor = request.user
    # base_on  = request.GET.get('base_on')
    postcode = request.GET.get('postcode')

    # If we have a postcode load nearby centres.
    if postcode:
        centres_qs = Centre.objects.all().near_postcode(postcode)[:8]
    else:
        centres_qs = Centre.objects.none()

    # Show the user the results
    return render_to_response(
        'certificates/select_centre.html',
        {
            'tutor':            tutor,
            'tutor_centres_qs': tutor.centres.all(),
            'postcode':         postcode, 
            'centres_qs':       centres_qs,
        },
        context_instance=RequestContext(request)
    )


@login_required
def create(request):
    """create a new certificate"""
    tutor    = request.user
    
    # we can't (easily) do this with generics as we need to pre-populate the
    # form if we are cloning an existing certificate.

    # If given a base_on try to load that certificate
    if request.GET.get('base_on'):
        # FIXME - add access controls
        base_certificate = get_object_or_404( Certificate, pk=request.GET.get('base_on') )
    else:
        base_certificate=None
    
    # try to get the centre from parameters or the base certificate - if none
    # found prompt the user for one.

    centre_id = request.REQUEST.get( 'centre_id', None )
    if centre_id:
        centre = get_object_or_404( Centre, pk=centre_id )
    elif base_certificate:
        centre = base_certificate.centre
    else:
        return redirect( select_centre )

    if request.method == 'POST':
        form = CertificateForm(
            request.POST,
            tutor            = tutor,
            base_certificate = base_certificate,
            centre           = centre,
        )
        
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.tutor = tutor
            certificate.save()
            return HttpResponseRedirect(
                reverse(
                    display,
                    kwargs={'certificate_id': certificate.id},
                )
            )            

    else:
        form = CertificateForm(
            tutor            = tutor,
            base_certificate = base_certificate,
            centre           = centre,
        )

    return render_to_response(
        'certificates/edit_certificate.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )

@login_required
def tutor_list(request, tutor_id):
    """Show all certificates for a particular user"""

    # 404 if user is not found
    certificate_tutor = get_object_or_404( Tutor, pk=tutor_id )
    
    check_user_may_see( request, certificate_tutor )
    
    # create the queryset
    queryset = certificate_tutor.certificate_set.order_by('-id')

    return object_list(
        request,
        template_name = 'certificates/tutor_list.html',
        paginate_by   = 40,
        allow_empty   = True,
        queryset      = queryset,
        extra_context = {
            "tutor": certificate_tutor,        
        },
    )
