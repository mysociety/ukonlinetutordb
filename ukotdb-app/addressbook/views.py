from addressbook.forms import CreateTutorForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, UserManager
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

def index(request):
    """show the homepage"""    
    return direct_to_template(
        request,
        template = 'addressbook/index.html',
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

            return HttpResponseRedirect( reverse( add_centres ) )
    else:
        form = CreateTutorForm()

    return render_to_response(
        'addressbook/create_tutor.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def add_centres(request):
    """Add all the centres"""

    
