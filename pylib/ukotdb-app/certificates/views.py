# import re
# 
# from tutordb.forms      import CreateTutorForm
# from tutordb.models     import Centre, Tenure, UserProfile
# 
# from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
# from django.contrib.auth.models         import User, UserManager
from django.core.urlresolvers           import reverse
# from django.db                          import IntegrityError
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template

from certificates.models import Certificate
from certificates.forms  import CertificateForm


@login_required
def index(request):
    """show the certificates nav page"""    
    
    return direct_to_template(
        request,
        template='certificates/index.html'
    )

@login_required
def display(request, certificate_id):
    """Display a certificate"""
    
    return object_detail(
        request,
        queryset  = request.user.certificate_set,
        object_id = certificate_id,
    )
    

@login_required
def create(request):
    """create a new certificate"""
    user = request.user
    
    # we can't (easily) do this with generics as we need to pre-populate the
    # form if we are cloning an existing certificate.
    
    # set up the initial data
    initial = {}
    
    if request.method == 'POST':
        form = CertificateForm(request.POST, user=user, initial=initial );
        
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.tutor = user
            certificate.save()
            return HttpResponseRedirect( reverse( display ) )            

    else:
        form = CertificateForm(user=user, initial=initial, )

    return render_to_response(
        'certificates/edit_certificate.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )
    