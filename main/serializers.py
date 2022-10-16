import shutil

from django.conf import settings

from rest_framework import serializers
from .models import Folder, File


class FileSerializer(serializers.ModelSerializer):
  class Meta:
    model = File 
    field = "__all__"


class FileListSerializer(serializers.Serializer):
  files = serializers.ListField(
    child = serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False)
  )
  folder = serializers.CharField(required=False)
  
  def zip_files(self, folder):
    shutil.make_archive(f"zip/{folder}", "zip", f"{settings.BASE_DIR}/media/{folder}")
  
  def create(self, validated_data):
    folder = Folder.objects.create()
    files = validated_data.pop("files")
    files_obj = []
    for file in files:
      file_obj = File.objects.create(folder=folder, file=file)
      files_obj.append(file_obj)
    
    self.zip_files(folder.uid)
    return {"files": {} , "folder": str(folder.uid)}