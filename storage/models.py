from django.db import models
from django.urls import reverse
from django.conf import settings

class Folder(models.Model):
      owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            related_name= 'folders'
      )
      name = models.CharField(max_length=255)
      parent = models.ForeignKey(
            "self", 
            on_delete= models.CASCADE,
            null=True, 
            blank=True, 
            related_name="children"
      )
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      
      class Meta:
            ordering = ['name']
      
      def __str__(self):
            return self.name
      
      def get_absolute_url(self):
            return reverse(
                  "storage:folder-detail",
                  kwargs={
                        "pk": self.pk,
                  },
            )

class File(models.Model):
      owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete= models.CASCADE,
            related_name= "files",
      )
      folder = models.ForeignKey(
            Folder,
            on_delete= models.CASCADE,
            related_name= "files",
      )
      file = models.FileField(upload_to="uploads/")
      original_name = models.CharField(max_length=255)
      file_type = models.CharField(max_length=100, blank=True)
      size = models.PositiveBigIntegerField(default=0)
      uploaded_at = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            ordering = ["-uploaded_at"]
            
      def __str__(self):
            return self.original_name