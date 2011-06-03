import re

from tutordb.forms      import CreateTutorForm, EditUserForm
from tutordb.models     import Centre, Tenure, UserProfile

from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
from django.contrib.auth.models         import User, UserManager, Group
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
        return HttpResponseRedirect( reverse( my ) )
    

    if request.method == 'POST':
        form = CreateTutorForm(request.POST)
        if form.is_valid():

            clean = form.cleaned_data

            # create a username from the email. In Django > 1.1 we could just
            # use the email address here.
            username = re.sub( '[^\w]+', '_', clean['email'] )

            # create the actual user and set the name
            user = User.objects.create_user( username, clean['email'], clean['password1'] )

            # put the whole name in the first_name field - better than trying
            # to split it and getting it wrong.
            user.first_name = clean['name']
            user.last_name  = ''

            # save the user.
            user.save()
            
            # create the user profile and store the phone number
            profile = UserProfile.objects.create( user=user, phone=clean['phone'] )
            profile.save()

            # jump through the Django hoops to the login
            login( request, authenticate( username=user.email, password=clean['password1'] ) )

            # FIXME - email the user their password

            return HttpResponseRedirect( reverse( add_centre ) )
    else:
        form = CreateTutorForm()

    return render_to_response(
        'tutordb/index.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )

@login_required
def my(request):
    """Homepage for a user"""
    
    user = request.user

    # get all the centres
    tenures = Tenure.objects.all().filter(user=user)
    centres = [ t.centre for t in tenures ]

    # get recent certificates
    certificates = user.certificate_set.order_by('-id').all()[:10]
        
    return render_to_response(
        'tutordb/my.html',
        {
            'centres':      centres,
            'certificates': certificates,
        },
        context_instance=RequestContext(request)
    )


@login_required
def edit_user_details(request):
    """Allow user to edit their own details"""

    user = request.user
    
    # we can't (easily) do this with generics as some details are in the user
    # objects, and some in the profile.

    if request.method == 'POST':

        form = EditUserForm(request.POST, user=user);
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            profile = user.get_profile()

            user.first_name = cleaned_data['name']
            user.last_name  = ''
            profile.phone   = cleaned_data['phone']

            user.save()
            profile.save()

            return HttpResponseRedirect( reverse( my ) )

    else:
        form = EditUserForm(user=user)

    return render_to_response(
        'tutordb/edit_user_details.html',
        {
            'form': form,
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
    
@login_required
def tutor_list(request, centre_id=None ):
    """Show list of centres for user to choose from"""

    user = request.user
    ho_group = Group.objects.get(name="Head Office")

    if centre_id:

        centre = get_object_or_404( Centre, pk=centre_id )

        # check that we are either in the HO group or that we are an admin for the centre
        if ho_group in user.groups.all() or user.is_admin_for( centre ):
            centre_tutor_ids = [ i.user.id for i in centre.tenure_set.all() ]
            queryset = User.objects.filter( id__in=centre_tutor_ids )
        else:
            queryset = User.objects.none()
        
        return object_list(
            request,
            template_name = 'tutordb/user_list.html',
            paginate_by   = 40,
            allow_empty   = True,
            queryset      = queryset,
        )
        
    else:
        if ho_group in user.groups.all():
            queryset = Centre.objects.all()
        else:
            user_admin_centres = user.tenure_set.filter( role='admin' )
            admin_ids = [ i.id for i in user_admin_centres ]
            queryset = Centre.objects.filter( id__in=admin_ids )
        
        
        return object_list(
            request,
            template_name = 'tutordb/user_centre_list.html',
            paginate_by   = 40,
            allow_empty   = True,
            queryset      = queryset,
        )

