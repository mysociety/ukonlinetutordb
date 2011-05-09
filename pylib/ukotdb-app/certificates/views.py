# import re
# 
# from tutordb.forms      import CreateTutorForm
# from tutordb.models     import Centre, Tenure, UserProfile
# 
# from django.contrib.auth                import authenticate, login
from django.contrib.auth.decorators     import login_required
# from django.contrib.auth.models         import User, UserManager
# from django.core.urlresolvers           import reverse
# from django.db                          import IntegrityError
# from django.http                        import HttpResponse, HttpResponseRedirect
# from django.shortcuts                   import render_to_response
# from django.template                    import RequestContext
# from django.views.generic.list_detail   import object_list, object_detail
from django.views.generic.simple        import direct_to_template


@login_required
def index(request):
    """show the certificates nav page"""    
    
    return direct_to_template(
        request,
        template='certificates/index.html'
    )

@login_required
def create(request):
    """show the certificates nav page"""    
    pass
