from django import forms
from .models import *

class postjobform(forms.Form):
    companyname = forms.CharField(max_length=30)
    jobtitle = forms.CharField(max_length=50)
    wtype = forms.CharField(max_length=30)
    jtype = forms.CharField(max_length=30)
    experience = forms.CharField(max_length=30)
    description = forms.CharField(max_length=300)

