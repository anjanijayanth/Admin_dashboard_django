# forms.py
from django import forms
from .models import Organization

class Org_Form(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'