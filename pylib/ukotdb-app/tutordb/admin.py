from django.contrib import admin
from tutordb import models
from django.contrib.auth.models import User

admin.site.register(models.Tenure)
admin.site.register(models.Centre)
admin.site.register(models.Tutor)

# Hide this so that people don't get confused
admin.site.unregister(User)