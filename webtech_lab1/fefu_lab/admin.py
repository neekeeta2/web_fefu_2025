from django.contrib import admin
from .models import Student, Instructor, Course, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'faculty', 'is_active', 'created_at']
    list_filter = ['is_active', 'faculty', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_editable = ['is_active']
    list_per_page = 20
    date_hierarchy = 'created_at'

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'specialization', 'is_active']
    list_filter = ['is_active', 'specialization']
    search_fields = ['first_name', 'last_name', 'email', 'specialization']
    list_per_page = 20

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'level', 'duration', 'price', 'is_active']
    list_filter = ['is_active', 'level', 'instructor']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'price']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'status']
    list_filter = ['status', 'enrolled_at', 'course']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    list_editable = ['status']
    list_per_page = 20
    date_hierarchy = 'enrolled_at'