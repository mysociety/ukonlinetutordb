from django.contrib.gis.db          import models
from django.contrib.auth.models     import User, UserManager
from django.db.models.signals       import post_save

# based on this blog article:
#   http://scottbarnham.com/blog/2008/08/21/extending-the-django-user-model-with-inheritance/

class Tutor(User):
    phone = models.CharField(max_length=20)
        
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

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
