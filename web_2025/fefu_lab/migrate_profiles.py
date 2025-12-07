import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_2025.settings')
django.setup()

from django.contrib.auth.models import User
from fefu_lab.models import Student, StudentProfile, TeacherProfile, AdminProfile, Instructor

def migrate_profiles():
    print("Начало миграции профилей...")
    
    for old_student in Student.objects.all():
        user = old_student.user
        if user:
            if old_student.role == 'STUDENT':
                # Создаем профиль студента
                StudentProfile.objects.create(
                    user=user,
                    role='STUDENT',
                    avatar=old_student.avatar,
                    phone=old_student.phone,
                    bio=old_student.bio,
                    is_active=old_student.is_active,
                    created_at=old_student.created_at,
                    updated_at=old_student.updated_at,
                    student_id=None,
                    birth_date=old_student.birth_date,
                    faculty=old_student.faculty,
                    year_of_study=1
                )
                print(f"Мигрирован студент: {user.email}")
            
            elif old_student.role == 'TEACHER':
                # Создаем профиль преподавателя
                teacher_profile = TeacherProfile.objects.create(
                    user=user,
                    role='TEACHER',
                    avatar=old_student.avatar,
                    phone=old_student.phone,
                    bio=old_student.bio,
                    is_active=old_student.is_active,
                    created_at=old_student.created_at,
                    updated_at=old_student.updated_at,
                    specialization='Требуется указать',
                    degree=''
                )
                
                # Создаем запись в Instructor
                instructor, created = Instructor.objects.get_or_create(
                    teacher_profile=teacher_profile,
                    defaults={'is_active': True}
                )
                print(f"Мигрирован преподаватель: {user.email}")
            
            elif old_student.role == 'ADMIN':
                # Создаем профиль администратора
                AdminProfile.objects.create(
                    user=user,
                    role='ADMIN',
                    avatar=old_student.avatar,
                    phone=old_student.phone,
                    bio=old_student.bio,
                    is_active=old_student.is_active,
                    created_at=old_student.created_at,
                    updated_at=old_student.updated_at,
                    admin_level='SUPER_ADMIN',
                    permissions={}
                )
                print(f"Мигрирован администратор: {user.email}")
    
    print("Миграция завершена!")

if __name__ == '__main__':
    migrate_profiles()