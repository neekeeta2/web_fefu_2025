import os
import sys
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from fefu_lab.models import Student, Course, Enrollment
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'
    
    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')
        
        # Очищаем существующие данные
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        Student.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Создаем пользователей и профили
        users_data = [
            {
                'username': 'teacher1',
                'email': 'teacher1@fefu.ru',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'role': 'TEACHER',
                'faculty': 'CS',
                'specialization': 'Кибербезопасность'
            },
            {
                'username': 'teacher2',
                'email': 'teacher2@fefu.ru',
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'role': 'TEACHER',
                'faculty': 'IT',
                'specialization': 'Веб-разработка'
            },
            {
                'username': 'admin1',
                'email': 'admin@fefu.ru',
                'first_name': 'Администратор',
                'last_name': 'Системы',
                'role': 'ADMIN',
                'faculty': 'CS'
            }
        ]
        
        teachers = []
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password123',  # Простой пароль для тестирования
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            student = Student.objects.create(
                user=user,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                role=user_data['role'],
                faculty=user_data['faculty']
            )
            
            if user_data['role'] == 'TEACHER':
                teachers.append(student)
            
            self.stdout.write(f'Создан пользователь: {user.username} ({user_data["role"]})')
        
        # Создаем студентов
        students_data = [
            {'first_name': 'Анна', 'last_name': 'Иванова', 'email': 'anna@fefu.ru', 'faculty': 'CS'},
            {'first_name': 'Дмитрий', 'last_name': 'Смирнов', 'email': 'dmitry@fefu.ru', 'faculty': 'SE'},
            {'first_name': 'Екатерина', 'last_name': 'Попова', 'email': 'ekaterina@fefu.ru', 'faculty': 'IT'},
            {'first_name': 'Михаил', 'last_name': 'Васильев', 'email': 'mikhail@fefu.ru', 'faculty': 'DS'},
            {'first_name': 'Ольга', 'last_name': 'Новикова', 'email': 'olga@fefu.ru', 'faculty': 'WEB'},
        ]
        
        students = []
        for student_data in students_data:
            # Создаем пользователя для студента
            username = student_data['email'].split('@')[0]
            user = User.objects.create_user(
                username=username,
                email=student_data['email'],
                password='password123',
                first_name=student_data['first_name'],
                last_name=student_data['last_name']
            )
            
            student = Student.objects.create(
                user=user,
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                email=student_data['email'],
                role='STUDENT',
                faculty=student_data['faculty'],
                birth_date=date(2000, 5, 15)
            )
            students.append(student)
        
        # Создаем курсы
        courses = [
            {
                'title': 'Основы Python',
                'slug': 'python-basics',
                'description': 'Базовый курс по программированию на языке Python.',
                'duration': 36,
                'instructor': teachers[0],
                'level': 'BEGINNER',
                'max_students': 25,
                'price': 0
            },
            {
                'title': 'Веб-безопасность',
                'slug': 'web-security',
                'description': 'Продвинутый курс по защите веб-приложений.',
                'duration': 48,
                'instructor': teachers[0],
                'level': 'ADVANCED',
                'max_students': 20,
                'price': 15000
            },
            {
                'title': 'Современный JavaScript',
                'slug': 'modern-javascript',
                'description': 'Изучение современных возможностей JavaScript.',
                'duration': 42,
                'instructor': teachers[1],
                'level': 'INTERMEDIATE',
                'max_students': 30,
                'price': 12000
            },
        ]
        
        created_courses = []
        for course_data in courses:
            course = Course.objects.create(**course_data)
            created_courses.append(course)
        
        # Создаем записи на курсы
        enrollments = [
            {'student': students[0], 'course': created_courses[0], 'status': 'ACTIVE'},
            {'student': students[0], 'course': created_courses[1], 'status': 'ACTIVE'},
            {'student': students[1], 'course': created_courses[0], 'status': 'ACTIVE'},
            {'student': students[1], 'course': created_courses[2], 'status': 'ACTIVE'},
            {'student': students[2], 'course': created_courses[0], 'status': 'ACTIVE'},
            {'student': students[3], 'course': created_courses[1], 'status': 'ACTIVE'},
            {'student': students[4], 'course': created_courses[2], 'status': 'ACTIVE'},
        ]
        
        for enrollment_data in enrollments:
            Enrollment.objects.create(**enrollment_data)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано: {User.objects.count()} пользователей, '
                f'{Student.objects.count()} профилей, {Course.objects.count()} курсов, '
                f'{Enrollment.objects.count()} записей на курсы'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\nТестовые учетные данные:\n'
                'Администратор: admin@fefu.ru / password123\n'
                'Преподаватель: teacher1@fefu.ru / password123\n'
                'Студент: anna@fefu.ru / password123'
            )
        )