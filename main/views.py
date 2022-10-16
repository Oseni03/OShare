from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import FileListSerializer

# Create your views here.
def home(request):
  if request.htmx:
    return render(request, "main/partials/button.html")
  return render(request, "main/home.html")


class HandleFileUpload(APIView):
  
  def post(self, request, *args, **kwargs):
    try:
      data = request.data 
      serializer = FileListSerializer(data=data)
      # if serializer.is_valid(raise_exception=True):
      if serializer.is_valid():
        serializer.save()
        return Response({
          "status": 200, 
          "message": "File uploaded successfully",
          "data": serializer.data
        })
      return Response({
        "status": 400, 
        "message": "Something went wrong", 
        "data": serializer.errors
      })
    except Exception as e:
      print(e)