from django.db import models

# Create your models here.
class BulkUpload(models.Model):
    FILE_TYPE_CHOICES = [
        ('video','Video'),
        ('audio','Audio'),
        ('csv','CSV'),
        ('doc','Word'),
        ('pdf','PDF'),
        ('xlsx','Excel'),
        ('other','Other')
    ]

    file    =   models.FileField(upload_to='uploads/')
    file_type   =   models.CharField(max_length=10,choices=FILE_TYPE_CHOICES,default='other')   
    uploaded_at =   models.DateTimeField(auto_now_add=True  )

    def __str__(self):
        return self.file.name