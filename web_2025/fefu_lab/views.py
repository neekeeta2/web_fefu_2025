from django.http import HttpResponse, Http404
from django.views import View

def home_page(request):
    return HttpResponse("""
        <h1>Добро пожаловать на главную страницу!</h1>
        <p><a href="/about/">О нас</a></p>
        <p><a href="/student/1/">Профиль студента 1</a></p>
        <p><a href="/student/50/">Профиль студента 50</a></p>
        <p><a href="/course/python-basic/">Курс Python Basic</a></p>
    """)

def about_page(request):
    return HttpResponse("""
        <h1>О нас</h1>
        <p>Это учебное приложение для лабораторной работы по Django.</p>
        <p><a href="/">На главную</a></p>
    """)

def student_profile(request, student_id):
    if student_id > 100:
        raise Http404("Студент с таким ID не найден")
    return HttpResponse(f"<h1>Профиль студента с ID: {student_id}</h1><p><a href='/'>На главную</a></p>")

class CourseDetailView(View):
    def get(self, request, course_slug):
        if course_slug not in ['python-basic', 'web-development']:
            raise Http404("Курс не найден")
        return HttpResponse(f"<h1>Курс: {course_slug}</h1><p><a href='/'>На главную</a></p>")