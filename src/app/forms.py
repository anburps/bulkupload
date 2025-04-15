from django import from .forms import 
from .models import *

class BulkUploadForm(forms.MOdelForm):
    class Meta:
        model = BulkUpload
        fields = "__all__"