from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from lms_core.models import Course, CourseContent
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg, Count

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello World</h1>")

def testing(request):
    dataCourse = Course.objects.all()
    dataCourse = serializers.serialize('python', dataCourse)
    
    return JsonResponse(dataCourse, safe=False)

def addData(request):
    try:
        teacher = User.objects.get(username="superadmin")
        course = Course(
            name="Course 1",
            description="Description",
            price=1000,
            teacher=teacher,
        )
        course.save()
        return JsonResponse({"status": "success", "message": "Data added successfully"})
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User 'superadmin' not found"}, status=404)

def editData(request):
    course = Course.objects.filter(name="coba coba").first()
    if course:
        course.name = "Course 2"
        course.save()
        return JsonResponse({"status": "success", "message": "Data edited successfully"})
    return JsonResponse({"status": "error", "message": "Course not found"}, status=404)

def deleteData(request):
    course = Course.objects.filter(name="Course 2").first()
    if course:
        course.delete()
        return JsonResponse({"status": "success", "message": "Data deleted successfully"})
    return JsonResponse({"status": "error", "message": "Course not found"}, status=404)

def allCourse(request):
    all_courses = Course.objects.all()
    result = [
        {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'price': course.price,
            'teacher': {
                'id': course.teacher.id,
                'username': course.teacher.username,
                'email': course.teacher.email,
                'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
            }
        }
        for course in all_courses
    ]
    return JsonResponse(result, safe=False)

def userCourses(request):
    try:
        user = User.objects.get(pk=3)
        courses = Course.objects.filter(teacher=user.id)
        course_data = [
            {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'price': course.price
            }
            for course in courses
        ]
        result = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'fullname': f"{user.first_name} {user.last_name}",
            'courses': course_data
        }
        return JsonResponse(result, safe=False)
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User not found"}, status=404)

def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    cheapest = Course.objects.filter(price=stats['min_price'])
    expensive = Course.objects.filter(price=stats['max_price'])
    popular = Course.objects.annotate(member_count=Count('coursemember')).order_by('-member_count')[:5]
    unpopular = Course.objects.annotate(member_count=Count('coursemember')).order_by('member_count')[:5]

    result = {
        'course_count': courses.count(),
        'courses': stats,
        'cheapest': [{'id': c.id, 'name': c.name, 'price': c.price} for c in cheapest],
        'expensive': [{'id': c.id, 'name': c.name, 'price': c.price} for c in expensive],
        'popular': [{'id': c.id, 'name': c.name, 'member_count': c.member_count} for c in popular],
        'unpopular': [{'id': c.id, 'name': c.name, 'member_count': c.member_count} for c in unpopular],
    }
    return JsonResponse(result, safe=False)

def courseMemberStat(request):
    courses = Course.objects.filter(description__contains='python').annotate(member_num=Count('coursemember'))
    course_data = [
        {
            'id': course.id,
            'name': course.name,
            'price': course.price,
            'member_count': course.member_num
        }
        for course in courses
    ]
    result = {'data_count': len(course_data), 'data': course_data}
    return JsonResponse(result)

def courseDetail(request, course_id):
    try:
        course = Course.objects.annotate(
            member_count=Count('coursemember'),
            content_count=Count('coursecontent'),
            comment_count=Count('coursecontent__comment')
        ).get(pk=course_id)
        
        contents = CourseContent.objects.filter(course_id=course.id).annotate(count_comment=Count('comment')).order_by('-count_comment')[:3]
        
        result = {
            "name": course.name,
            'description': course.description,
            'price': course.price,
            'member_count': course.member_count,
            'content_count': course.content_count,
            'teacher': {
                'username': course.teacher.username,
                'email': course.teacher.email,
                'fullname': course.teacher.first_name
            },
            'comment_stat': {
                'comment_count': course.comment_count,
                'most_comment': [
                    {'name': content.name, 'comment_count': content.count_comment}
                    for content in contents
                ]
            },
        }
        return JsonResponse(result)
    except Course.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Course not found"}, status=404)
