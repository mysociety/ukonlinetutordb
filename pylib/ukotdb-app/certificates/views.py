# import re
# 
# from tutordb.forms      import CreateTutorForm
# 
# from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
# from django.contrib.auth.models         import User, UserManager
from django.core.urlresolvers           import reverse
# from django.db                          import IntegrityError
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response, get_object_or_404
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template

from certificates.models import Certificate
from certificates.forms  import CertificateForm


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
    

@login_required
def display(request, certificate_id):
    """Display a certificate"""
    
    # FIXME - add access controls

    return object_detail(
        request,
        queryset  = request.user.certificate_set,
        object_id = certificate_id,
    )
    

@login_required
def display_as_pdf(request, certificate_id):
    """Create a PDF for certificate"""

    # get the certificate
    # FIXME - add access controls
    certificate = get_object_or_404( Certificate, pk=certificate_id )
    
    # create the pdf
    pdf = certificate.as_pdf()

    # set up the response for pdf
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=certificate_%s.pdf' % certificate_id
    response.write(pdf)
    return response


@login_required
def create(request):
    """create a new certificate"""
    user = request.user
    
    # we can't (easily) do this with generics as we need to pre-populate the
    # form if we are cloning an existing certificate.

    # If given a base_on try to load that certificate
    if request.GET.get('base_on'):
        # FIXME - add access controls
        base_certificate = get_object_or_404( Certificate, pk=request.GET.get('base_on') )
    else:
        base_certificate=None
    
    if request.method == 'POST':
        form = CertificateForm(request.POST, user=user, base_certificate=base_certificate );
        
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.tutor = user
            certificate.save()
            return HttpResponseRedirect(
                reverse(
                    display,
                    kwargs={'certificate_id': certificate.id},
                )
            )            

    else:
        form = CertificateForm(user=user, base_certificate=base_certificate )

    return render_to_response(
        'certificates/edit_certificate.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
    