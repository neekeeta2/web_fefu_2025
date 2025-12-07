from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Course, Instructor, Enrollment, Profile
from .forms import FeedbackForm, EnrollmentForm, CustomAuthenticationForm, StudentRegistrationForm, TeacherRegistrationForm, ProfileForm


def home_page(request):
    """Главная страница с статистикой"""
    total_students = Profile.objects.filter(role='STUDENT', is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    return render(request, 'fefu_lab/home.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_courses': recent_courses
    })


def about_page(request):
    """Страница 'О нас'"""
    return render(request, 'fefu_lab/about.html')



def login_view(request):
    """Вход в систему"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Устанавливаем бэкенд вручную
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                
                next_page = request.GET.get('next', 'profile')
                return redirect(next_page)
            else:
                messages.error(request, 'Неверные имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'fefu_lab/registration/login.html', {'form': form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')




def register_view(request):
    """Регистрация нового студента"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Сохраняем пользователя и профиль через форму
                user = form.save()
                
                # Устанавливаем бэкенд для пользователя
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                # ИЛИ используйте ваш кастомный бэкенд:
                user.backend = 'fefu_lab.backends.EmailBackend'
                
                # Автоматический вход после регистрации
                login(request, user)
                messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {user.first_name}!')
                return redirect('profile')
                
            except IntegrityError:
                messages.error(request, 'Пользователь с таким именем или email уже существует.')
            except Exception as e:
                messages.error(request, f'Произошла ошибка при регистрации: {str(e)}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'fefu_lab/registration/register.html', {'form': form})


# ========== ПРОФИЛЬ И ЛИЧНЫЕ КАБИНЕТЫ ==========



@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Создаем профиль, если его нет
        profile = Profile.objects.create(user=request.user, role='STUDENT')
    
    if profile.role == 'STUDENT':
        enrollments = Enrollment.objects.filter(student=profile, status='ACTIVE')
        return render(request, 'fefu_lab/dashboard/student_dashboard.html', {
            'profile': profile,
            'enrollments': enrollments
        })
    
    elif profile.role == 'TEACHER':
        try:
            instructor = Instructor.objects.get(profile=profile)
            courses = Course.objects.filter(instructor=instructor, is_active=True)
        except Instructor.DoesNotExist:
            courses = Course.objects.none()
            instructor = None
        
        # Формируем список курсов с информацией о записях
        courses_with_enrollments = []
        for course in courses:
            enrollments = Enrollment.objects.filter(course=course, status='ACTIVE')
            courses_with_enrollments.append({
                'course': course,
                'enrollments': enrollments,
                'enrollment_count': enrollments.count()
            })
        
        return render(request, 'fefu_lab/dashboard/teacher_dashboard.html', {
            'profile': profile,
            'instructor': instructor,
            'courses_with_enrollments': courses_with_enrollments
        })
    
    elif profile.role == 'ADMIN':
        total_students = Profile.objects.filter(role='STUDENT').count()
        total_teachers = Profile.objects.filter(role='TEACHER').count()
        total_courses = Course.objects.count()
        total_enrollments = Enrollment.objects.count()
        
        return render(request, 'fefu_lab/dashboard/admin_dashboard.html', {
            'profile': profile,
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments
        })
    
    return redirect('home')




@login_required
def profile_edit_view(request):
    """Редактирование профиля"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, role='STUDENT')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'fefu_lab/registration/profile_edit.html', {'form': form})


# ========== ОСТАЛЬНЫЕ ПРЕДСТАВЛЕНИЯ ==========

def student_list(request):
    """Список всех студентов"""
    students = Profile.objects.filter(role='STUDENT', is_active=True).order_by('user__last_name')
    return render(request, 'fefu_lab/student_list.html', {'students': students})


def student_detail(request, pk):
    """Детальная информация о студенте"""
    student = get_object_or_404(Profile, pk=pk, role='STUDENT')
    enrollments = student.enrollments.filter(status='ACTIVE')
    return render(request, 'fefu_lab/student_detail.html', {
        'student': student,
        'enrollments': enrollments
    })


def course_list(request):
    """Список всех курсов"""
    courses = Course.objects.filter(is_active=True)
    return render(request, 'fefu_lab/course_list.html', {'courses': courses})


def course_detail(request, slug):
    """Детальная информация о курсе"""
    course = get_object_or_404(Course, slug=slug)
    enrollments = course.enrollments.filter(status='ACTIVE')
    return render(request, 'fefu_lab/course_detail.html', {
        'course': course,
        'enrollments': enrollments
    })


def feedback_view(request):
    """Обратная связь"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Спасибо за ваше сообщение!')
            return redirect('home')
    else:
        form = FeedbackForm()
    
    return render(request, 'fefu_lab/feedback.html', {'form': form})


@login_required
def enrollment_view(request):
    """Запись на курс"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, 'Профиль не найден.')
        return redirect('profile')
    
    if profile.role != 'STUDENT':
        messages.error(request, 'Только студенты могут записываться на курсы.')
        return redirect('profile')
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = profile
            enrollment.status = 'ACTIVE'
            
            # Проверяем, не записан ли уже на курс
            if Enrollment.objects.filter(student=profile, course=enrollment.course, status='ACTIVE').exists():
                messages.error(request, 'Вы уже записаны на этот курс!')
            else:
                enrollment.save()
                messages.success(request, f'Вы успешно записались на курс "{enrollment.course.title}"!')
                return redirect('profile')
    else:
        form = EnrollmentForm()
    
    # Получаем доступные курсы
    available_courses = Course.objects.filter(is_active=True)
    return render(request, 'fefu_lab/enrollment.html', {
        'form': form,
        'available_courses': available_courses
    })