import logging

from django   import forms
from datetime import datetime

from certificates.models import Certificate, CertificateTemplate
from tutordb.models      import Centre

class CertificateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """setup the tutor and the centre"""

        tutor            = kwargs.pop('tutor')
        centre           = kwargs.pop('centre')
        base_certificate = kwargs.pop('base_certificate')

        # create the form as normal
        super( CertificateForm, self ).__init__(*args, **kwargs)

        # set the centre choices
        tenure_qs = tutor.tenure_set.all()
        centre_ids = [ centre.id ]
        centre_ids += [ o.centre.id for o in tenure_qs ]
        centre_qs = Centre.objects.filter( id__in=centre_ids)
        self.fields['centre'] = forms.ModelChoiceField(queryset=centre_qs, empty_label=None)

        # limit templates to those that are active
        self.fields['template'] = forms.ModelChoiceField(
            queryset=CertificateTemplate.objects.filter( active=True ),
            empty_label=None
        )

        # set some initial values
        if base_certificate:
            self.fields['template'].initial     = base_certificate.template.id
            # student name deliberately left out
            self.fields['date_awarded'].initial = base_certificate.date_awarded
            self.fields['tutor_name'].initial   = base_certificate.tutor_name
            self.fields['centre'].initial       = base_certificate.centre.id
            self.fields['course_name'].initial  = base_certificate.course_name
            self.fields['course_blurb'].initial = base_certificate.course_blurb
        else:
            self.fields['date_awarded'].initial = datetime.now
            self.fields['tutor_name'].initial   = tutor.get_full_name()

        

    class Meta:
        model = Certificate
        fields = (
            'template',
            'student_name',
            'date_awarded',
            'tutor_name',
            'centre',
            'course_name',
            'course_blurb',
        )
        widgets = {
            'course_blurb': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }

class CertificateEmailForm(forms.Form):

    to        = forms.EmailField( required=True )
    subject   = forms.CharField( required=True, initial="Your certificate" )
    message   = forms.CharField( required=True, widget=forms.Textarea )

    def __init__(self, *args, **kwargs):

        certificate = kwargs.pop('certificate')

        # create the form as normal
        super( CertificateEmailForm, self ).__init__(*args)

        self.fields['message'].initial = (
            "Dear %s,\n\nAttached please find your certificate.\n\nYours,\n  %s\n"
                % ( certificate.student_name, certificate.tutor.get_full_name() ) )



