from django.views.generic.list_detail import object_list, object_detail

from tutordb.models import Centre

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
    

