import re
from django import forms

from django.contrib.auth.models import User


class CreateTutorForm(forms.Form):
    email     = forms.EmailField( required=True )
    name      = forms.CharField( required=True )
    phone     = forms.CharField( required=True )
    password1 = forms.CharField( required=True, label="Password",         widget=forms.PasswordInput() )
    password2 = forms.CharField( required=True, label="Password Confirm", widget=forms.PasswordInput() )

    
    def clean_email(self):
        """Check that the email is not already taken"""
        email = self.cleaned_data['email']
    
        # lowercase the email
        email = email.lower()
    
        if User.objects.all().filter(email=email).count():
            raise forms.ValidationError("Email address already has an account - perhaps you should log in?")
    
        return email

    def clean(self):
            cleaned_data = self.cleaned_data
            p1 = cleaned_data.get("password1")
            p2 = cleaned_data.get("password2")
    
            if p1 != p2:
                msg = u"The two passwords do not match."
                self._errors["password2"] = self.error_class([msg])
    
            # Always return the full collection of cleaned data.
            return cleaned_data