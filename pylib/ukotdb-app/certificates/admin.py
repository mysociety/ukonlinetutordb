from django.contrib import admin
from certificates.models import Certificate, CertificateTemplate

class CertificateAdmin(admin.ModelAdmin):
    list_display = ( 'student_name', 'course_name', 'tutor_name', )

admin.site.register(Certificate, CertificateAdmin)
admin.site.register(CertificateTemplate)
