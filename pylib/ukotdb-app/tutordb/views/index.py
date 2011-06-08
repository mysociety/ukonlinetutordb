import re

from tutordb.forms      import CreateTutorForm, EditTutorForm
from tutordb.models     import Centre, Tenure, Tutor
import tutordb.views.my

from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
from django.core.urlresolvers           import reverse
from django.db                          import IntegrityError
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response, get_object_or_404
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template

def index(request):
    """show the homepage"""    
    
    # if the user is logged in send them to 'my' straight away
    if request.user.is_authenticated():
        return HttpResponseRedirect( reverse( tutordb.views.my.my ) )

    # force the creation of a session so that the CSRF protection is enabled.
    request.session['force_on'] = True    
    
    if request.method == 'POST':
        form = CreateTutorForm(request.POST)
        if form.is_valid():
    
            clean = form.cleaned_data
    
            # create a username from the email. In Django > 1.1 we could just
            # use the email address here.
            username = re.sub( '[^\w]+', '_', clean['email'] )
    
            # create the actual user and set the name
            tutor = Tutor.objects.create_user( username, clean['email'], clean['password1'] )
    
            # put the whole name in the first_name field - better than trying
            # to split it and getting it wrong.
            tutor.first_name = clean['name']
            tutor.last_name  = ''
            tutor.phone=clean['phone']
    
            # save the tutor.
            tutor.save()
            
            # jump through the Django hoops to the login
            login( request, authenticate( username=tutor.email, password=clean['password1'] ) )
    
            # FIXME - email the tutor their password
    
            return HttpResponseRedirect( reverse( tutordb.views.my.add_centre ) )
    else:
        form = CreateTutorForm()

    return render_to_response(
        'tutordb/index.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )

