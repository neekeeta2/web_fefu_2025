from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from .forms import FeedbackForm, RegistrationForm, LoginForm
from .models import UserProfile, Feedback

# def home_page(request):
#     return HttpResponse("Добро пожаловать на главную страницу!")

# def about_page(request):
#     return HttpResponse("Страница о нас:")

# def student_profile(request, student_id):
#     if student_id > 100:
#         raise Http404("Студент не найден")
#     return HttpResponse(f"Профиль студента с ID: {student_id}")

# def course_detail(request, course_slug):
#     return HttpResponse(f"Информация о курсе: {course_slug}")


STUDENTS_DATA = {
    1: {
        'info': 'Иван Петров',
        'faculty': 'Кибербезопасность',
        'status': 'Активный',
        'year': 3
    },
    2: {
        'info': 'Мария Сидорова', 
        'faculty': 'Информатика',
        'status': 'Активный',
        'year': 2
    },
    3: {
        'info': 'Алексей Козлов',
        'faculty': 'Программная инженерия', 
        'status': 'Выпускник',
        'year': 5
    }
}

COURSES_DATA = {
    'python-basics': {
        'name': 'Основы программирования на Python',
        'duration': 36,
        'description': 'Базовый курс по программированию на языке Python для начинающих.',
        'instructor': 'Доцент Петров И.С.',
        'level': 'Начальный'
    },
    'web-security': {
        'name': 'Веб-безопасность',
        'duration': 48,
        'description': 'Курс по защите веб-приложений от современных угроз.',
        'instructor': 'Профессор Сидоров А.В.',
        'level': 'Продвинутый'
    },
    'network-defense': {
        'name': 'Защита сетей',
        'duration': 42,
        'description': 'Изучение методов и технологий защиты компьютерных сетей.',
        'instructor': 'Доцент Козлова М.П.',
        'level': 'Средний'
    }
}

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

def student_profile(request, student_id):
    if student_id in STUDENTS_DATA:
        student_data = STUDENTS_DATA[student_id]
        return render(request, 'fefu_lab/student_profile.html', {
            'title': f'Студент {student_id}',
            'heading': f'Профиль студента',
            'student_id': student_id,
            'student_info': student_data['info'],
            'faculty': student_data['faculty'],
            'status': student_data['status'],
            'year': student_data['year']
        })
    else:
        raise Http404("Студент с таким ID не найден")

def course_detail(request, course_slug):
    if course_slug in COURSES_DATA:
        course_data = COURSES_DATA[course_slug]
        return render(request, 'fefu_lab/course_detail.html', {
            'title': course_data['name'],
            'heading': course_data['name'],
            'course_slug': course_slug,
            'course_name': course_data['name'],
            'duration': course_data['duration'],
            'description': course_data['description'],
            'instructor': course_data['instructor'],
            'level': course_data['level']
        })
    else:
        raise Http404("Курс не найден")

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

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            UserProfile.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']  # В реальном проекте хешируйте пароль!
            )
            return render(request, 'fefu_lab/success.html', {
                'title': 'Регистрация',
                'heading': 'Регистрация завершена',
                'message': 'Поздравляем! Вы успешно зарегистрировались в системе.'
            })
    else:
        form = RegistrationForm()
    
    return render(request, 'fefu_lab/register.html', {
        'title': 'Регистрация',
        'heading': 'Форма регистрации',
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