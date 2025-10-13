from django.http import HttpResponse, Http404
from django.shortcuts import render

def home_page(request):
    return HttpResponse("Добро пожаловать на главную страницу!")

def about_page(request):
    return HttpResponse("Страница о нас:")

def student_profile(request, student_id):
    if student_id > 100:
        raise Http404("Студент не найден")
    return HttpResponse(f"Профиль студента с ID: {student_id}")

def course_detail(request, course_slug):
    return HttpResponse(f"Информация о курсе: {course_slug}")