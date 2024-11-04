from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from lms_core.models import Course
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello World</h1>")

def testing(request):
    dataCourse = Course.objects.all()
    dataCourse = serializers.serialize('python', dataCourse)
    
    return JsonResponse(dataCourse, safe=False)

def addData(request):
    course = Course(
        name = "Course 1",
        description = "Description",
        price = 1000,
        teacher = User.objects.get(username="superadmin"),
    )
    course.save()
    return JsonResponse({"status": "success", "message": "Data added successfully"})

def editData(request):
    course = Course.objects.filter(name="coba coba").first()
    course.name = "Course 2"
    course.save()
    return JsonResponse({"status": "success", "message": "Data edited successfully"})

def deleteData(request):
    course = Course.objects.filter(name="Course 2").first()
    course.delete()
    return JsonResponse({"status": "success", "message": "Data deleted successfully"})