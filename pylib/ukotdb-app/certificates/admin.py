from django.contrib import admin
from certificates import models

admin.site.register(models.Certificate)
admin.site.register(models.CertificateTemplate)
