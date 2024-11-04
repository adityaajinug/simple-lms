from django.contrib import admin
from lms_core.models import Course
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'teacher', 'created_at']
    list_filter = ['name', 'description', 'price', 'teacher', 'created_at']
    search_fields = ['name', 'description', 'teacher']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['name', 'description', 'price', 'image', 'teacher', 'created_at', 'updated_at']