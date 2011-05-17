from django   import forms
from datetime import datetime

from certificates.models import Certificate
from tutordb.models      import Centre

class CertificateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """setup the tutor and the centre"""

        user = kwargs.pop('user')

        # create the form as normal
        super( CertificateForm, self ).__init__(*args, **kwargs)

        # set the centre choices
        tenure_qs = user.tenure_set.all()
        centre_ids = [ o.centre.id for o in tenure_qs ]
        centre_qs = Centre.objects.filter( id__in=centre_ids)
        self.fields['centre'] = forms.ModelChoiceField(queryset=centre_qs, empty_label=None)

        # limit templates to those that are active
        # TODO - code this
        # self.fields['template'] = forms.ModelChoiceField(queryset=...., empty_label=None)

        # set some initial values
        self.fields['tutor_name'].initial   = user.get_full_name()
        self.fields['date_awarded'].initial = datetime.now

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
