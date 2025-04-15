from django.shortcuts import render,redirect
from .forms import *
from .models import *

# Create your views here.
def upload_file(request):
    if request.method == "POST":
        form    =   BulkUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload success')
    else:
        form    =   BulkUploadForm()
    
    return render(request,'upload.html',{'form':form})