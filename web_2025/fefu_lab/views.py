from django.shortcuts import render
from .forms import FeedbackForm, RegistrationForm

# Данные для студентов и курсов (добавь в начало файла)
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
    'web-development': {
        'name': 'Web Development',
        'duration': 48,
        'description': 'Разработка веб-приложений на Django.',
        'instructor': 'Профессор Сидоров А.В.',
        'level': 'Продвинутый'
    }
}


def home_page(request):
    return render(request, 'fefu_lab/home.html')

def about_page(request):
    return render(request, 'fefu_lab/about.html')

def student_profile(request, student_id):
    if student_id in STUDENTS_DATA:
        student_data = STUDENTS_DATA[student_id]
        return render(request, 'fefu_lab/student_profile.html', {
            'student_id': student_id,
            'student_info': student_data['info'],
            'faculty': student_data['faculty'],
            'status': student_data['status'],
            'year': student_data['year']
        })
    else:
        from django.http import Http404
        raise Http404("Студент с таким ID не найден")

def course_detail(request, course_slug):
    if course_slug in COURSES_DATA:
        course_data = COURSES_DATA[course_slug]
        return render(request, 'fefu_lab/course_detail.html', {
            'course_slug': course_slug,
            'course_name': course_data['name'],
            'duration': course_data['duration'],
            'description': course_data['description'],
            'instructor': course_data['instructor'],
            'level': course_data['level']
        })
    else:
        from django.http import Http404
        raise Http404("Курс не найден")
    



def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Здесь можно сохранить данные в БД, когда она будет
            return render(request, 'fefu_lab/success.html', {
                'message': 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.',
                'title': 'Обратная связь'
            })
    else:
        form = FeedbackForm()
    
    return render(request, 'fefu_lab/feedback.html', {
        'form': form,
        'title': 'Обратная связь'
    })

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Здесь можно сохранить пользователя в БД
            return render(request, 'fefu_lab/success.html', {
                'message': 'Регистрация прошла успешно! Добро пожаловать!',
                'title': 'Регистрация'
            })
    else:
        form = RegistrationForm()
    
    return render(request, 'fefu_lab/register.html', {
        'form': form,
        'title': 'Регистрация'
    })