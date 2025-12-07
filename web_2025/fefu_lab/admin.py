from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Instructor, Course, Enrollment


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    extra = 0
    max_num = 1
    
    def get_fieldsets(self, request, obj=None):
        return [
            ('Роль пользователя', {
                'fields': ['role', 'is_active']
            }),
            ('Общая информация', {
                'fields': ['avatar', 'phone', 'bio']
            }),
        ]


class CustomUserAdmin(BaseUserAdmin):
    # Показываем ProfileInline ТОЛЬКО при редактировании существующего пользователя
    def get_inlines(self, request, obj=None):
        if obj and hasattr(obj, 'profile'):
            return [ProfileInline]
        return []

    list_display = ('username', 'email', 'get_full_name', 'get_role', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}" if obj.first_name or obj.last_name else obj.username
    get_full_name.short_description = 'ФИО'
    
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except Profile.DoesNotExist:
            return "Нет профиля"
    get_role.short_description = 'Роль'


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'role', 'get_additional_info', 'is_active']
    list_filter = ['is_active', 'role', 'faculty', 'department', 'admin_level', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'student_id']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_full_name(self, obj):
        # Показываем ФИО из модели User, если оно есть
        if obj.user.first_name or obj.user.last_name:
            return f"{obj.user.last_name} {obj.user.first_name}"
        return obj.user.username
    get_full_name.short_description = 'ФИО'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    # Динамически меняем поля в зависимости от роли
    def get_fieldsets(self, request, obj=None):
        if obj:
            fieldsets = [
                ('Основная информация', {
                    'fields': ['user', 'role', 'is_active']
                }),
                ('Общая информация', {
                    'fields': ['avatar', 'phone', 'bio']
                }),
            ]
            
            if obj.role == 'STUDENT':
                fieldsets.append(('Студенческие данные', {
                    'fields': ['student_id', 'faculty', 'year_of_study', 'birth_date']
                }))
            elif obj.role == 'TEACHER':
                fieldsets.append(('Профессиональные данные', {
                    'fields': ['specialization', 'degree', 'academic_rank', 'department', 'office']
                }))
            elif obj.role == 'ADMIN':
                fieldsets.append(('Административные данные', {
                    'fields': ['admin_level']
                }))
            
            fieldsets.append(('Системная информация', {
                'fields': ['created_at', 'updated_at'],
                'classes': ['collapse']
            }))
            
            return fieldsets
        
        # При создании нового профиля
        return [
            ('Основная информация', {
                'fields': ['user', 'role', 'is_active']
            }),
            ('Общая информация', {
                'fields': ['avatar', 'phone', 'bio']
            }),
        ]
    
    def get_additional_info(self, obj):
        if obj.role == 'STUDENT':
            faculty_display = obj.get_faculty_display_name() if obj.faculty else "Не указан"
            return f"{faculty_display} - {obj.year_of_study or '?'} курс"
        elif obj.role == 'TEACHER':
            return f"{obj.specialization}" if obj.specialization else "Специализация не указана"
        elif obj.role == 'ADMIN':
            return f"{obj.get_admin_level_display_name()}"
        return "-"
    get_additional_info.short_description = 'Доп. информация'


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'get_specialization', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['profile__user__first_name', 'profile__user__last_name', 'profile__user__email']
    list_editable = ['is_active']
    
    # Улучшенный селект для выбора профиля преподавателя
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'profile':
            # Показываем только профили преподавателей
            kwargs['queryset'] = Profile.objects.filter(role='TEACHER')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_full_name(self, obj):
        # Прямой доступ к данным пользователя
        if obj.profile.user.first_name or obj.profile.user.last_name:
            return f"{obj.profile.user.last_name} {obj.profile.user.first_name}"
        return obj.profile.user.username
    get_full_name.short_description = 'ФИО'
    
    def email(self, obj):
        return obj.profile.user.email
    email.short_description = 'Email'
    
    def get_specialization(self, obj):
        return obj.profile.specialization if obj.profile.specialization else "Не указана"
    get_specialization.short_description = 'Специализация'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_instructor_name', 'level', 'duration', 'price', 'is_active', 'enrolled_students_count', 'available_slots']
    list_filter = ['is_active', 'level', 'instructor']
    search_fields = ['title', 'description', 'instructor__profile__user__first_name', 'instructor__profile__user__last_name']
    list_editable = ['is_active', 'price']
    readonly_fields = ['created_at', 'updated_at', 'enrolled_students_count', 'available_slots']
    
    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.profile.user.last_name} {obj.instructor.profile.user.first_name}"
        return "Не назначен"
    get_instructor_name.short_description = 'Преподаватель'
    
    def enrolled_students_count(self, obj):
        return obj.enrolled_students_count
    enrolled_students_count.short_description = 'Записанных студентов'
    
    def available_slots(self, obj):
        return obj.available_slots
    available_slots.short_description = 'Свободных мест'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'get_course_title', 'enrolled_at', 'status', 'grade']
    list_filter = ['status', 'enrolled_at', 'course']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'course__title']
    list_editable = ['status', 'grade']
    readonly_fields = ['enrolled_at', 'completed_at']
    
    # Улучшенный селект для выбора студентов
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            # Показываем только профили студентов
            kwargs['queryset'] = Profile.objects.filter(role='STUDENT')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_student_name(self, obj):
        return f"{obj.student.user.last_name} {obj.student.user.first_name}"
    get_student_name.short_description = 'Студент'
    
    def get_course_title(self, obj):
        return obj.course.title
    get_course_title.short_description = 'Курс'
    
    # Поля в форме
    fieldsets = [
        ('Основная информация', {
            'fields': ['student', 'course', 'status', 'grade']
        }),
        ('Даты', {
            'fields': ['enrolled_at', 'completed_at'],
            'classes': ['collapse']
        }),
    ]
    
    # Автоматически устанавливаем completed_at при завершении курса
    def save_model(self, request, obj, form, change):
        if obj.status == 'COMPLETED' and not obj.completed_at:
            from django.utils import timezone
            obj.completed_at = timezone.now()
        super().save_model(request, obj, form, change)