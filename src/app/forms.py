# forms.py
from django import forms
from .models import UploadeFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadeFile
        fields = ['name', 'file']
