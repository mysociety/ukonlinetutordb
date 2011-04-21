import re
from django import forms

from django.contrib.auth.models import User


class CreateTutorForm(forms.Form):
    username   = forms.CharField( min_length=4, max_length=30, required=True)
    email      = forms.EmailField( required=True )
    first_name = forms.CharField( required=True )
    last_name  = forms.CharField( required=True )
    
    def clean_username(self):
        """Check that the username is correctly formatted and not already taken"""
        username = self.cleaned_data['username']
        
        # lowercase the username
        username = username.lower().strip()

        if re.search('[^a-z0-9_]', username):
            raise forms.ValidationError("Invalid - only a-z, 0-9 and '_' allowed")

        if User.objects.all().filter(username=username).count():
            raise forms.ValidationError("Username already taken - please choose another")

        return username

    def clean_email(self):
        """Check that the email is not already taken"""
        email = self.cleaned_data['email']
    
        # lowercase the email
        email = email.lower()
    
        if User.objects.all().filter(email=email).count():
            raise forms.ValidationError("Email address already has an account - perhaps you should log in?")
    
        return email
