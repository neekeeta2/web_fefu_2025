from .models import StudentProfile, TeacherProfile, AdminProfile, Instructor

def get_user_profile(user):
    """Получить профиль пользователя"""
    # Пробуем получить профиль студента
    try:
        return user.studentprofile
    except StudentProfile.DoesNotExist:
        pass
    
    # Пробуем получить профиль преподавателя
    try:
        return user.teacherprofile
    except TeacherProfile.DoesNotExist:
        pass
    
    # Пробуем получить профиль администратора
    try:
        return user.adminprofile
    except AdminProfile.DoesNotExist:
        pass
    
    return None