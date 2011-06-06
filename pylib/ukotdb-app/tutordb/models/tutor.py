import logging

from django.contrib.gis.db          import models
from django.contrib.auth.models     import User, UserManager, Group
from django.db.models.signals       import post_save

# based on this blog article:
#   http://scottbarnham.com/blog/2008/08/21/extending-the-django-user-model-with-inheritance/

class Tutor(User):
    phone = models.CharField(max_length=20)
        
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def is_head_office(self):
        """docstring for is_head_office"""
        ho_group = Group.objects.get(name="Head Office")

        # check that we are either in the HO group or that we are an admin for the centre
        if ho_group in self.groups.all():
            return True
        else:
            return False

    def is_manager_of(self, underling):
        """Check if the user is manager of another user"""
        underling_centres = [ i.centre for i in underling.tenure_set.all() ]
        manager_centres   = [ i.centre for i in self.tenure_set.filter(role='admin').all() ]

        for man_centre in manager_centres:
            if man_centre in underling_centres:
                return True

        return False
        
            

    def __unicode__(self):
        return self.email
    

    class Meta:
        app_label = 'tutordb'



# TODO - When a User is created directly (eg during the initial db sync) no
# matching tutor is created. This means that the user cannot log in until an
# entry in the 'tutors' table is created.
#
# This should ideally be done using signals - but not going to attempt that code
# until we have a stable django version to target.
