from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from .forms import FeedbackForm, RegistrationForm, LoginForm
from .models import UserProfile, Feedback, Instructor, Course, Enrollment, Student
from django.db import IntegrityError

# Существующие представления
def home(request):
    return render(request, 'fefu_lab/home.html', {
        'title': 'Главная страница',
        'heading': 'Добро пожаловать в учебную систему'
    })

def about(request):
    return render(request, 'fefu_lab/about.html', {
        'title': 'О нас',
        'heading': 'О нашей образовательной платформе'
    })

# Новые представления для форм
@csrf_protect
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Сохраняем feedback в базу данных
            Feedback.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            return render(request, 'fefu_lab/success.html', {
                'title': 'Обратная связь',
                'heading': 'Сообщение отправлено',
                'message': 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.'
            })
    else:
        form = FeedbackForm()
    
    return render(request, 'fefu_lab/feedback.html', {
        'title': 'Обратная связь',
        'heading': 'Форма обратной связи',
        'form': form
    })



# @csrf_protect
# def register_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             # Создаем пользователя
#             UserProfile.objects.create(
#                 username=form.cleaned_data['username'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password']  # В реальном проекте хешируйте пароль!
#             )
#             return render(request, 'fefu_lab/success.html', {
#                 'title': 'Регистрация',
#                 'heading': 'Регистрация завершена',
#                 'message': 'Поздравляем! Вы успешно зарегистрировались в системе.'
#             })
#     else:
#         form = RegistrationForm()
    
#     return render(request, 'fefu_lab/register.html', {
#         'title': 'Регистрация',
#         'heading': 'Форма регистрации',
#         'form': form
#     })



@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Создаем студента (пароль не сохраняем в этой модели)
                student = form.save()
                
                return render(request, 'fefu_lab/success.html', {
                    'title': 'Регистрация',
                    'heading': 'Регистрация завершена',
                    'message': f'Поздравляем, {student.first_name}! Вы успешно зарегистрировались как студент.'
                })
            except IntegrityError as e:
                if 'email' in str(e):
                    form.add_error('email', 'Студент с таким email уже существует')
                else:
                    form.add_error(None, 'Произошла ошибка при регистрации')
    else:
        form = RegistrationForm()
    
    return render(request, 'fefu_lab/register.html', {
        'title': 'Регистрация',
        'heading': 'Регистрация студента',
        'form': form
    })


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return render(request, 'fefu_lab/success.html', {
                'title': 'Вход в систему',
                'heading': 'Вход выполнен',
                'message': 'Вы успешно вошли в систему!'
            })
    else:
        form = LoginForm()
    
    return render(request, 'fefu_lab/login.html', {
        'title': 'Вход в систему',
        'heading': 'Вход в систему',
        'form': form
    })



@csrf_protect
def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'fefu_lab/instructor_list.html', {
        'title': 'Преподаватели',
        'heading': 'Наши преподаватели',
        'instructors': instructors,
    })



@csrf_protect
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'fefu_lab/course_list.html', {
        'title': 'Курсы',
        'heading': 'Наши курсы', 
        'courses': courses,
    })



# @csrf_protect
# def enrollment_view(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
    
#     if request.method == 'POST':
#         student_name = request.POST.get('student_name')
#         student_email = request.POST.get('student_email')
        
#         if student_name and student_email:
#             try:
#                 # Создаем студента
#                 student = Student.objects.create(
#                     first_name=student_name.split()[0] if ' ' in student_name else student_name,
#                     last_name=student_name.split()[1] if ' ' in student_name else '',
#                     email=student_email,
#                     faculty='CS'
#                 )
                
#                 # Записываем на курс
#                 Enrollment.objects.create(
#                     student=student,
#                     course=course,
#                     status='ACTIVE'
#                 )
                
#                 return render(request, 'fefu_lab/success.html', {
#                     'title': 'Запись на курс',
#                     'heading': 'Запись успешна!',
#                     'message': f'{student_name}, вы успешно записаны на курс "{course.title}"!'
#                 })
                
#             except IntegrityError:
#                 return render(request, 'fefu_lab/enrollment.html', {
#                     'title': f'Запись на курс: {course.title}',
#                     'heading': f'Запись на курс: {course.title}',
#                     'course': course,
#                     'error': 'Студент с таким email уже существует'
#                 })
    
#     return render(request, 'fefu_lab/enrollment.html', {
#         'title': f'Запись на курс: {course.title}',
#         'heading': f'Запись на курс: {course.title}',
#         'course': course,
#     })



@csrf_protect
def enrollment_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.filter(is_active=True)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        
        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                
                # Проверяем, не записан ли уже студент на этот курс
                if Enrollment.objects.filter(student=student, course=course).exists():
                    return render(request, 'fefu_lab/enrollment.html', {
                        'title': f'Запись на курс: {course.title}',
                        'heading': f'Запись на курс: {course.title}',
                        'course': course,
                        'students': students,
                        'error': f'{student.first_name} уже записан на этот курс'
                    })
                
                # Записываем на курс
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    status='ACTIVE'
                )
                
                return render(request, 'fefu_lab/success.html', {
                    'title': 'Запись на курс',
                    'heading': 'Запись успешна!',
                    'message': f'{student.first_name} {student.last_name}, вы успешно записаны на курс "{course.title}"!'
                })
                
            except Student.DoesNotExist:
                return render(request, 'fefu_lab/enrollment.html', {
                    'title': f'Запись на курс: {course.title}',
                    'heading': f'Запись на курс: {course.title}',
                    'course': course,
                    'students': students,
                    'error': 'Студент не найден'
                })
        else:
            return render(request, 'fefu_lab/enrollment.html', {
                'title': f'Запись на курс: {course.title}',
                'heading': f'Запись на курс: {course.title}',
                'course': course,
                'students': students,
                'error': 'Пожалуйста, выберите студента'
            })
    
    return render(request, 'fefu_lab/enrollment.html', {
        'title': f'Запись на курс: {course.title}',
        'heading': f'Запись на курс: {course.title}',
        'course': course,
        'students': students,
    })



def student_list(request):
    students = Student.objects.all()
    return render(request, 'fefu_lab/student_list.html', {
        'title': 'Студенты',
        'heading': 'Наши студенты',
        'students': students,
    })