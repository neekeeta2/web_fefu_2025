from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps

def student_required(function=None):
    """
    Декоратор для проверки, что пользователь - студент
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            
            # Проверяем роль в профиле
            if hasattr(request.user, 'profile'):
                if request.user.profile.role == 'STUDENT':
                    return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("Доступ запрещен. Требуется роль студента.")
        return _wrapped_view
    
    if function:
        return decorator(function)
    return decorator


def teacher_required(function=None):
    """
    Декоратор для проверки, что пользователь - преподаватель
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            
            if hasattr(request.user, 'profile'):
                if request.user.profile.role == 'TEACHER':
                    return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("Доступ запрещен. Требуется роль преподавателя.")
        return _wrapped_view
    
    if function:
        return decorator(function)
    return decorator


def admin_required(function=None):
    """
    Декоратор для проверки, что пользователь - администратор
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            
            if hasattr(request.user, 'profile'):
                if request.user.profile.role == 'ADMIN':
                    return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("Доступ запрещен. Требуется роль администратора.")
        return _wrapped_view
    
    if function:
        return decorator(function)
    return decorator