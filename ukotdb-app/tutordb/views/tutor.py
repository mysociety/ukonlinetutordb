from tutordb.forms      import CreateTutorForm
from tutordb.models     import Centre, Tenure

from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
from django.contrib.auth.models         import User, UserManager
from django.core.urlresolvers           import reverse
from django.db                          import IntegrityError
from django.http                        import HttpResponse, HttpResponseRedirect
from django.shortcuts                   import render_to_response
from django.template                    import RequestContext
from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template

def index(request):
    """show the homepage"""    
    return direct_to_template(
        request,
        template = 'tutordb/index.html',
    )

def create_tutor(request):
    """Let someone sign up as a new tutor"""

    if request.method == 'POST':
        form = CreateTutorForm(request.POST)
        if form.is_valid():

            clean = form.cleaned_data

            # create the actual user and set the name
            user = User.objects.create_user( clean['username'], clean['email'] )
            user.first_name = clean['first_name']
            user.last_name  = clean['last_name']

            # create a password so that we can log them in
            password = UserManager().make_random_password()
            user.set_password( password )
            user.save()

            # jump through the Django hoops to the login
            login( request, authenticate( username=user.username, password=password ) )

            # FIXME - email the user their password

            return HttpResponseRedirect( reverse( my ) )
    else:
        form = CreateTutorForm()

    return render_to_response(
        'tutordb/create_tutor.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required
def my(request):
    """Homepage for a user"""
    
    user = request.user
    tenures = Tenure.objects.all().filter(user=user)
    centres = [ t.centre for t in tenures ]
        
    return render_to_response(
        'tutordb/my.html',
        {
            'centres' : centres,
        },
        context_instance=RequestContext(request)
    )
    
@login_required
def add_centre(request):
    """Allow a user to add a centre to themselves"""
    
    # declare in case it gets used
    error = None
    
    # If we have a post then add centre to user and redirect back to '/my'
    centre_id = request.POST.get('centre_id')
    if centre_id:
        try:
            centre = Centre.objects.get(id=centre_id)
            centre.tenure_set.create(user=request.user, role='tutor')
        except Centre.DoesNotExist:
            error = "Could not find centre in db";
        except IntegrityError:
            # centre and user already linked - do nothing
            pass
            
        if not error:
            return HttpResponseRedirect( reverse( my ) )

    # FIXME - search for name as well?
    postcode = request.GET.get('postcode')    
    if postcode:
        queryset = Centre.objects.all().near_postcode(postcode)
    else:
        queryset = Centre.objects.none()
    
    return object_list(
        request,
        template_name = 'tutordb/add_centre.html',
        paginate_by   = 20,
        allow_empty   = True,
        queryset      = queryset,
        extra_context = {
            'postcode' : postcode,
            'error'    : error,
        },
    )
    