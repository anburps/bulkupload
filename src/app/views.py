# views.py
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
from .models import UploadeFile

@csrf_exempt
def upload_file_view(request):
    if request.method == 'POST':
        file = request.FILES['file']
        filename = request.POST.get('filename')
        chunk_index = request.POST.get('chunkIndex')
        total_chunks = request.POST.get('totalChunks')

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
        os.makedirs(upload_dir, exist_ok=True)

        chunk_path = os.path.join(upload_dir, f'{filename}.part{chunk_index}')
        with open(chunk_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        print("chunk uploaded", chunk_path)
        if int(chunk_index) + 1 == int(total_chunks):
            final_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
            with open(final_path, 'wb+') as final_file:

                for i in range(int(total_chunks)):
                    print("merging", i)
                    part_path = os.path.join(upload_dir, f'{filename}.part{i}')
                    with open(part_path, 'rb') as part_file:
                        final_file.write(part_file.read())
                    os.remove(part_path)

            UploadeFile.objects.create(name=filename, file=f'uploads/{filename}')
            return redirect('upload_success')
        return JsonResponse({'message': 'Chunk uploaded'})

    return render(request, 'upload.html')



def upload_success(request):
    return render(request, 'success.html')

from django.shortcuts import render, redirect
from .forms import UploadFileForm
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import UploadeFile

@csrf_exempt
def home(request):
    if request.method == 'POST':
        file = request.FILES['file']
        filename = request.POST.get('filename')
        chunk_index = request.POST.get('chunkIndex')
        total_chunks = request.POST.get('totalChunks')

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'temp_chunks')
        os.makedirs(upload_dir, exist_ok=True)

        chunk_path = os.path.join(upload_dir, f'{filename}.part{chunk_index}')
        with open(chunk_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        print("chunk uploaded", chunk_path)

        if int(chunk_index) + 1 == int(total_chunks):
            # Final file path under media/home/
            final_dir = os.path.join(settings.MEDIA_ROOT, 'home')
            os.makedirs(final_dir, exist_ok=True)
            final_path = os.path.join(final_dir, filename)

            with open(final_path, 'wb+') as final_file:
                for i in range(int(total_chunks)):
                    print("merging", i)
                    part_path = os.path.join(upload_dir, f'{filename}.part{i}')
                    with open(part_path, 'rb') as part_file:
                        final_file.write(part_file.read())
                    os.remove(part_path)

            # Save record in database
            UploadeFile.objects.create(name=filename, file=f'home/{filename}')

            # Send JSON response with redirect URL
            return JsonResponse({'message': 'Upload complete', 'redirect_url': '/success/'})

        # Normal chunk response
        return JsonResponse({'message': 'Chunk uploaded'})

    return render(request, 'home.html')